# 🌸 StudyBloom AI — RAG Study Assistant

StudyBloom AI is an AI-powered study assistant that uses **Retrieval-Augmented Generation (RAG)** to answer questions from user-provided study materials.

Instead of relying only on the LLM's general knowledge, StudyBloom AI retrieves relevant information from uploaded documents and uses that context to generate accurate, document-grounded responses.

---

## 🚀 Features

- 📄 Upload and process study documents
- ✂️ Text extraction and document chunking
- 🔎 Semantic similarity-based document retrieval
- 🧠 Embedding-based knowledge search
- 🤖 LLM-powered question answering
- 📚 Source/context-based responses
- 🖥️ Interactive Streamlit interface
- 📊 Evaluation pipeline for testing RAG responses
- 🔐 Environment-variable based API configuration

---

## 🏗️ Architecture

```text
                Study Materials
                       │
                       ▼
              ┌─────────────────┐
              │ Document Loader │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Chunking     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Embeddings    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Vector Store   │
              └────────┬────────┘
                       │
                  User Question
                       │
                       ▼
              ┌─────────────────┐
              │    Retrieval    │
              └────────┬────────┘
                       │
                 Relevant Context
                       │
                       ▼
              ┌─────────────────┐
              │       LLM       │
              └────────┬────────┘
                       │
                       ▼
                Generated Answer    
