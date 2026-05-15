# PDF-Query
A Lang-chain project using Cassandra DB supported by Google Gemini AI model and API. Showcase use RAG pipeline for usage of PDF source for answering the input queries

## Dataflow Diagram

```mermaid
graph TD
    subgraph Ingestion_Flow
        A[PDF Document] --> B[Reading the Document - Text Extraction & Splitting]
        B --> C[Text Chunks]
        C --> D[Google Gemini Embeddings]
        D --> E[Vector Database (Cassandra/Astra DB)]
    end

    subgraph Query_Flow
        F[Human] --> G[Text + Query]
        G -- "Similarity Search (Text + Embeddings)" --> E[Vector Database (Cassandra/Astra DB)]
        E -- "DataStax Vector Search" --> H[Text embeddings(Relevant context)]
        H --> I[Google Gemini LLM]
        G --> I
        I --> J[Final Answer]
    end

```

# Resources
- Datastack



