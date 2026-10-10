# Architecture

```text
Student / Mentor
      |
 Streamlit Frontend
      |
 FastAPI API Layer
      |
      +-- Context (optional intern ID)
      +-- Retrieval engine
      |     +-- FAQ chunks
      |     +-- Case-study chunks
      |     +-- keyword-overlap ranking
      +-- Progress / skill-gap rules
            +-- sample intern profiles
            +-- mentor feedback
            +-- weekly learning plan
```

## RAG approach
This is a minimal RAG-style baseline: local documents are stored as chunks, relevant chunks are retrieved for a question, and the response is constructed from those chunks. To keep setup light, retrieval uses lexical term overlap rather than transformer embeddings or an external vector database. A future version can replace this module with sentence-transformers plus FAISS/Chroma and a grounded LLM.

## Human oversight
- If no useful source is found, the assistant abstains rather than guessing.
- The included intern data is synthetic sample data.
- Mentors make final performance and task-allocation decisions.
