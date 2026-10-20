# 📚 Research Assistant (RAG)

A Retrieval-Augmented Generation (RAG) based Research Assistant that enables users to organize research papers into projects, perform semantic search, ask natural language questions, and generate structured paper summaries with the Google Gemini API.

Built using **Python, FAISS, Sentence Transformers for local embeddings, Google Gemini, FastAPI, and Streamlit**.

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
- Sentence Transformers for local embeddings
- Google Gemini API (`google-genai`) for answer generation
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
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

`GEMINI_MODEL` is optional and defaults to `gemini-3.5-flash-lite`. The application calls the Gemini `models.generate_content` API. Set the same names in Streamlit Secrets when deploying.

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

## Deploy a public demo

The Streamlit UI can be deployed on [Streamlit Community Cloud](https://share.streamlit.io/) directly from this GitHub repository. Embeddings and FAISS retrieval run locally; answer generation uses the Google Gemini API.

1. Sign in to Streamlit Community Cloud with GitHub and select **Create app**.
2. Choose this repository, the `main` branch, and `ui/app.py` as the app file.
3. Open **Advanced settings** and select Python `3.11`.
4. In the **Secrets** field, add:

      ```toml
      GEMINI_API_KEY = "your_gemini_api_key"
      GEMINI_MODEL = "gemini-3.5-flash-lite"
      PUBLIC_DEMO_MODE = "true"
      ```

      Create a key in [Google AI Studio](https://aistudio.google.com/apikey). Do not put the key in GitHub or frontend code.
5. Deploy, wait for the build to finish, then open the `*.streamlit.app` URL shown by Community Cloud.

`PUBLIC_DEMO_MODE=true` gives each browser session a separate temporary project workspace. Uploaded documents and indexes are not persistent and are removed when the hosting process restarts. Public visitors can upload research documents; do not upload sensitive or confidential PDFs. Retrieved document text is sent to Google Gemini for answer generation.

Review Gemini API usage and project rate limits before sharing the app widely. Community Cloud apps can sleep after 12 hours without traffic, and its published resource limits are approximately 2 CPU cores and up to 2.7 GB RAM; the local embedding model and PyTorch dependencies can make startup and indexing slower on the free shared tier.

The root `requirements.txt` is UTF-8 encoded and also contains the dependencies for the separately run FastAPI backend. This deployment starts only the Streamlit UI; to run the API locally, use the existing command below.

## Checking Gemini quota and access

Open the [Google AI Studio Rate limits page](https://aistudio.google.com/rate-limit) for the same Google project used by `GEMINI_API_KEY`. Check the configured model's active limits and usage for **RPM** (requests per minute), **TPM** (input tokens per minute), and **RPD** (requests per day), along with whether that model is eligible on the **Free tier**. Limits are project- and model-specific; RPD resets at midnight Pacific time. If an API call returns 429, the status alone does not establish that RPD was exhausted: compare the project's usage against each active limit and inspect the full error in the application log.

The app makes one generation request per chat, summary, or research-gap action and disables SDK retries. The Google error and AI Studio project limits are the evidence to use when diagnosing quota failures; do not infer daily exhaustion from a rate-limit message alone.

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
      (FAISS + Embeddings)   (Google Gemini)

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