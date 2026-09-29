🌸 StudyBloom AI
StudyBloom AI is an AI-powered RAG (Retrieval-Augmented Generation) study assistant that allows students to upload PDF notes and ask questions directly from their study material.

The application retrieves relevant information from the uploaded documents and uses an LLM to generate concise answers with source citations.

🚀 Live Demo
👉 Try StudyBloom AI

Upload your study notes, build the knowledge index, and ask questions based on your documents.

✨ Features
📚 Upload PDF study notes
🔎 Search relevant information from documents
🤖 AI-powered question answering
🌸 Simple and attractive pink-themed Streamlit interface
💬 Interactive chat interface
📌 Answers include source references such as [1], [2]
🧠 Semantic search using sentence embeddings
⚡ FAISS-based vector search
🚀 Groq LLM integration
🔐 API keys stored securely using environment variables
🛠️ Tech Stack
Python
Streamlit – Web application interface
FAISS – Vector similarity search
Sentence Transformers – Text embeddings
Groq – LLM inference
OpenAI Python SDK – API communication
pypdf – PDF processing
python-dotenv – Environment variable management
🏗️ Project Structure
StudyBloom-AI-rag-assistant/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── data/
│   └── .gitkeep
│
├── eval/
│   ├── evaluate.py
│   └── questions.json
│
└── rag/
    ├── __init__.py
    ├── ingest.py
    ├── store.py
    └── generate.py
🔄 How It Works
StudyBloom AI uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions from uploaded study notes.

Step 1: 📄 Upload Notes
The user uploads a PDF containing study material through the Streamlit interface.

Step 2: ✂️ Text Extraction & Chunking
The PDF content is extracted and divided into smaller text chunks so that relevant information can be searched efficiently.

Step 3: 🧠 Create Embeddings
Each text chunk is converted into a numerical representation using Sentence Transformers.

Step 4: 🔎 Store & Search
The embeddings are stored in a FAISS vector index. When the user asks a question, the system searches the index to find the most relevant passages.

Step 5: 🤖 Generate Answer
The retrieved passages are provided as context to the Groq-powered LLM.

Step 6: 💬 Display Response
The LLM generates a concise answer based on the retrieved document content, along with source references such as [1] and [2].

Complete Flow
📄 PDF Notes
      ↓
✂️ Text Extraction & Chunking
      ↓
🧠 Sentence Transformer Embeddings
      ↓
🔎 FAISS Vector Search
      ↓
📚 Relevant Context
      ↓
🤖 Groq LLM
      ↓
💬 Answer + Source Citations