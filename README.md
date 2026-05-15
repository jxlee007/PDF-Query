# PDF-Query
A Lang-chain project using Cassandra DB supported by Google Gemini AI model and API. Showcase use RAG pipeline for usage of PDF source for answering the input queries

## Dataflow Diagram

```mermaid
graph TD
    subgraph Ingestion_Flow
        A[PDF Document] --> B[Text Extraction & Splitting]
        B --> C[Text Chunks]
        C --> D[Google Gemini Embeddings]
        D --> E[(Cassandra DB - Vector Store)]
    end

    subgraph Query_Flow
        F[User Query] --> G[Google Gemini Embeddings]
        G --> H[Similarity Search]
        H --> I[Text embeddings]
        E --> I
        I --> J[Google Gemini LLM]
        F --> J
        J --> K[Final Answer]
    end
```

# Resources
- Datastack



