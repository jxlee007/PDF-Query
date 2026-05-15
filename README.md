# PDF-Query
A Lang-chain project using Cassandra DB supported by Google Gemini AI model and API. Showcase use RAG pipeline for usage of PDF source for answering the input queries

## Dataflow Diagram

```mermaid
graph TD
    subgraph Ingestion_Flow
        A[PDF Document] --> B["Reading the Document (Text Extraction & Splitting)"]
        B --> C[Text Chunks]
        C --> D[Google Gemini Embeddings]
        D --> E["Vector Database (Cassandra/Astra DB)"]
    end

    subgraph Query_Flow
        F[Human] --> G["Text + Query"]
        G -- "Similarity Search" --> E
        E -- "DataStax Vector Search" --> H["Text embeddings \n(Relevant context)"]
        H --> I[Google Gemini LLM]
        G --> I
        I --> J[Final Answer]
    end


```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file based on `.env.example` and add your credentials:
   - `ASTRA_DB_APPLICATION_TOKEN`
   - `ASTRA_DB_ID`
   - `GOOGLE_API_KEY`

## How to Run

Launch the Streamlit application:
```bash
streamlit run app.py
```

## Features
- **Dynamic PDF Upload**: Upload any PDF to query its content.
- **Astra DB Integration**: Powered by DataStax for high-performance vector search.
- **Google Gemini AI**: Uses state-of-the-art models for embeddings and text generation.

# Resources
- [DataStax Astra DB](https://astra.datastax.com/)
- [Google AI Studio](https://aistudio.google.com/)
- [LangChain Documentation](https://python.langchain.com/)
