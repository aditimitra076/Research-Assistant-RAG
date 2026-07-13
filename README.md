# 📚 Research Assistant (RAG)

A Retrieval-Augmented Generation (RAG) based Research Assistant that allows users to create projects, upload research papers, build vector indexes, ask natural language questions, and generate structured summaries using Large Language Models.

---

## ✨ Features

- 📁 Multiple research projects
- 📄 Upload one or more PDFs
- 🔍 Semantic search using FAISS
- 🤖 LLM-powered Question Answering
- 📝 Automatic Paper Summarization
- 🔎 Typo-tolerant Retrieval
- 📚 Source Citations
- 📊 Confidence-based Answer Filtering
- ⚡ FastAPI backend
- 🎨 Streamlit interface

---

## 🛠 Tech Stack

- Python
- Streamlit
- FastAPI
- FAISS
- Sentence Transformers
- Hugging Face Inference API
- PyPDF
- RapidFuzz

---

## 📂 Project Structure

```text
Research_Assistant_RAG/
│
├── api/                 # FastAPI backend
├── data/                # Sample PDFs
├── modules/             # Core RAG pipeline
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── generator.py
│   ├── project_manager.py
│   ├── project_indexer.py
│   └── ...
│
├── projects/            # User-created projects
├── ui/                  # Streamlit frontend
│   ├── components/
│   └── pages/
│
├── requirements.txt
└── README.md
```

## ⚙️ Installation

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

Windows

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

## 🚀 Running the Application

Start the Streamlit frontend

```bash
streamlit run ui/app.py
```

(Optional) Start the FastAPI backend

```bash
uvicorn api.main:app --reload
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

## 🔄 Workflow

1. Create a Project
2. Upload one or more Research Papers
3. Build the Vector Index
4. Ask Natural Language Questions
5. Retrieve Relevant Chunks
6. Generate Answers using Llama 3.1
7. Generate Structured Paper Summaries


## ✅ Current Features

- Multiple Project Management
- PDF Upload
- Automatic Chunking
- Sentence Embeddings
- FAISS Vector Search
- Typo-Tolerant Retrieval
- Metadata-aware Retrieval
- Confidence-based Filtering
- Source Citations
- Research Paper Summarization
- FastAPI REST API
- Streamlit User Interface

## 🏗️ System Architecture

```text
                +----------------------+
                |   Streamlit UI       |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   RAG Engine         |
                +----------+-----------+
                           |
        +------------------+------------------+
        |                                     |
        v                                     v
+------------------+               +----------------------+
| Retriever        |               | Generator (LLM)      |
| FAISS +          |               | Llama 3.1            |
| SentenceEncoder  |               | HuggingFace API      |
+--------+---------+               +----------+-----------+
         |                                     ^
         v                                     |
+------------------------+                     |
| Chunked PDF Embeddings |---------------------+
+------------------------+
         ^
         |
+------------------------+
| Uploaded PDFs          |
+------------------------+
```

## 🚀 Future Improvements

- Hybrid Search (BM25 + Dense Retrieval)
- Cross Encoder Re-ranking
- Research Gap Detection
- Citation Export
- Multi-document Comparison
- OCR Support for Scanned PDFs
- Local LLM Support
- Docker Deployment

## 👩‍💻 Author

**Aditi Mitra**

MCA'27 • University of Hyderabad

Interests:
- Retrieval-Augmented Generation (RAG)
- Machine Learning
- AI Systems
- NLP

## 📄 License

This project is intended for educational and portfolio purposes.