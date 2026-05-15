import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_community.vectorstores import Cassandra
from langchain_classic.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import cassio

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="PDF Query Assistant", page_icon="📄", layout="wide")

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    .stButton > button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        border-radius: 5px;
    }
    .stFileUploader {
        border: 1px dashed #4b4b4b;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_app():
    """Initialize Astra DB connection and model configurations."""
    # Get credentials from .env or sidebar
    astra_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    astra_id = os.getenv("ASTRA_DB_ID")
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not all([astra_token, astra_id, google_api_key]):
        st.error("Missing configuration. Please ensure .env file is set up correctly.")
        st.stop()

    # Initialize CassIO
    cassio.init(token=astra_token, database_id=astra_id)
    
    # Initialize LLM and Embeddings
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key, temperature=0.3)
    embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=google_api_key)
    
    return llm, embedding

def process_pdf(uploaded_file, embedding):
    """Extract text from PDF, split into chunks, and index in Astra DB."""
    with st.spinner("Processing PDF..."):
        pdf_reader = PdfReader(uploaded_file)
        raw_text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                raw_text += content
        
        # Split text
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_text(raw_text)
        
        # Initialize Vector Store
        # Note: Using a unique table name or letting user specify might be better
        # For now, following notebook's pattern
        astra_vector_store = Cassandra(
            embedding=embedding,
            table_name="pdf_query_demo", # Using a more descriptive name
            session=None,
            keyspace=None,
        )
        
        # Add texts to store
        astra_vector_store.add_texts(texts[:50]) # Limiting to 50 as in notebook
        
        # Wrap with index wrapper
        index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)
        return index

def main():
    st.title("🤖 PDF AI Query Assistant")
    st.markdown("---")

    llm, embedding = initialize_app()

    # Sidebar for PDF Upload
    with st.sidebar:
        st.header("Settings")
        uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
        if uploaded_file:
            if "index" not in st.session_state:
                st.session_state.index = process_pdf(uploaded_file, embedding)
                st.success("PDF Indexed Successfully!")
        
        if st.button("Clear Session"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

    # Main Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your PDF..."):
        if "index" not in st.session_state:
            st.warning("Please upload a PDF first.")
        else:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Use the index wrapper to query
                        # VectorStoreIndexWrapper usually has a query method
                        response = st.session_state.index.query(prompt, llm=llm)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Error generating response: {e}")

if __name__ == "__main__":
    main()
