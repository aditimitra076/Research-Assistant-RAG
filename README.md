# 📚 Research Assistant (RAG)

A Retrieval-Augmented Generation (RAG) based Research Assistant that enables users to organize research papers into projects, perform semantic search, ask natural language questions, and generate structured paper summaries using Large Language Models.

Built using **Python, FAISS, Sentence Transformers, Hugging Face LLMs, FastAPI, and Streamlit**.

---

# ✨ Features

- 📁 Multiple Project Management
- 📄 Upload one or multiple research papers (PDF)
- ⚡ Automatic PDF indexing
- 🔍 Semantic Retrieval using FAISS
- 🤖 LLM-powered Question Answering
- 📝 Structured Paper Summaries
- 🔎 Typo-tolerant Query Retrieval
- 📑 Metadata-aware Retrieval (authors, title, conference, etc.)
- 📚 Source Citations
- 📊 Confidence-based Answer Filtering
- ⚡ REST API using FastAPI
- 🎨 Interactive Streamlit Interface

---

# 🛠 Tech Stack

### Backend
- Python
- FastAPI

### Frontend
- Streamlit

### RAG Pipeline
- FAISS
- Sentence Transformers
- Hugging Face Inference API
- PyPDF
- RapidFuzz

### Utilities
- NumPy
- Pickle
- dotenv

---

# 📂 Project Structure

```text
Research_Assistant_RAG/
│
├── api/                  # FastAPI backend
├── modules/              # Core RAG pipeline
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── retriever.py
│   ├── generator.py
│   ├── vector_store.py
│   ├── project_manager.py
│   ├── project_indexer.py
│   └── ...
│
├── projects/             # User-created projects
├── ui/                   # Streamlit interface
│   ├── components/
│   └── pages/
│
├── assets/               # Application screenshots
├── requirements.txt
├── README.md
└── .env
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>
cd Research_Assistant_RAG
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
HF_TOKEN=your_huggingface_api_key
```

---

# 🚀 Running the Application

## Streamlit UI

```bash
streamlit run ui/app.py
```

Open

```
http://localhost:8501
```

---

## FastAPI Backend

```bash
uvicorn api.main:app --reload
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

# 🔄 Workflow

```text
Create Project
      ↓
Upload PDFs
      ↓
Build FAISS Index
      ↓
User Question
      ↓
Typo Correction
      ↓
Semantic Retrieval
      ↓
LLM Answer Generation
      ↓
Answer + Sources
```

---

# ✅ Implemented Features

- Multiple Project Management
- Search Projects
- Delete Projects
- Upload Multiple PDFs
- Automatic Chunking
- Sentence Embeddings
- FAISS Vector Search
- Typo-Tolerant Retrieval
- Metadata-aware Retrieval
- Confidence-based Retrieval Filtering
- Source Citation Generation
- Paper Summarization
- FastAPI REST API
- Streamlit User Interface

---

# 🏗 System Architecture

```text
                    Streamlit UI
                          │
                          ▼
                   RAG Engine
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
         Retriever           Generator
    (FAISS + Embeddings)      (Llama 3.1)

                ▲
                │
         Chunked PDF Embeddings
                ▲
                │
           Uploaded PDFs
```

---

# 📸 Screenshots

Application screenshots are available inside the **assets/** folder.

They include:

- Home Page
- Project Dashboard
- Upload Workflow
- Question Answering
- Paper Summary
- API Documentation (Swagger)

---

# 🚀 Future Improvements

- Hybrid Retrieval (BM25 + Dense Search)
- Cross-Encoder Re-ranking
- Research Gap Detection
- Multi-paper Comparison
- Citation Export
- OCR Support
- Local LLM Integration
- Docker Deployment
- Complete Frontend–API Separation

---

# 👩‍💻 Author

**Aditi Mitra**

MCA '27 • University of Hyderabad

Interests

- Retrieval-Augmented Generation (RAG)
- Machine Learning
- NLP
- AI Systems

---

# 📄 License

This project is intended for educational, learning, and portfolio purposes.