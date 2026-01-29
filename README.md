# 📚 Teaching Assistant Chatbot (Multimodal RAG)

A **multimodal Retrieval-Augmented Generation (RAG) chatbot** that helps students ask natural-language questions and receive accurate, textbook-grounded answers from **large, image-rich academic PDFs**.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture & Design](#architecture--design)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Workflow / Pipeline Explanation](#workflow--pipeline-explanation)
- [Configuration](#configuration)
- [Future Improvements](#future-improvements)
- [Why This Design?](#why-this-design)
- [Contributing](#contributing)

---

## 🧠 Overview

The **Teaching Assistant Chatbot** is an AI-powered assistant designed to help students query large educational textbooks in a **reliable and explainable** way.

### Real-world Use Case

- Students asking conceptual or visual questions from **school or college textbooks**
- Teachers validating answers against source material
- Self-study from scanned PDFs containing **text, tables, and images**

### Why This Project Is Non-Trivial

- Handles **2 large PDFs (800+ pages total)**
- Supports **multimodal data** (text, tables, images)
- Optimized for **memory-efficient ingestion**
- Uses **local LLMs (Ollama)** → no external API dependency
- Designed to scale beyond demo-size RAG systems

This is **not** a toy RAG — it is built for real academic data.

---

## ✨ Key Features

- 🔍 **Multimodal RAG**
  - Text, tables, and image-aware retrieval
- 🧠 **Local LLM Inference**
  - Uses Ollama (`llava:7b`) for privacy and cost efficiency
- 📚 **Large PDF Support**
  - Efficient ingestion of hundreds of pages
- 🗂️ **Vector Store Persistence**
  - ChromaDB with disk-backed storage
- 🧩 **Modular Design**
  - Clear separation of ingestion, embeddings, prompts, and RAG logic
- ⚡ **Optimized Memory Usage**
  - Batch processing during ingestion
- 🖥️ **Simple UI**
  - Streamlit-based frontend for students

---

## 🏗️ Architecture & Design

### High-Level Flow

1. **PDF Ingestion**
   - PDFs are partitioned using `unstructured`
   - Content is extracted as:
     - Text blocks
     - Tables
     - Images

2. **Summarization Layer**
   - Each modality is summarized separately
   - Reduces token size while preserving meaning

3. **Embedding & Storage**
   - Summaries are embedded using `OllamaEmbeddings`
   - Stored in **ChromaDB** with metadata (`type`, `doc_id`)

4. **Query Time (RAG)**
   - User asks a question via Streamlit
   - Relevant chunks are retrieved
   - Separate reasoning for:
     - Text + Tables
     - Images
   - Final answer is merged and returned

### Why This Architecture?

- Avoids loading entire PDFs into memory
- Allows modality-specific reasoning
- Keeps LLM prompts clean and controllable
- Easy to extend with new document types

---

## 🧰 Tech Stack

### Backend / Core

- Python 3.10+
- LangChain

### AI / ML

- Ollama (`llava:7b`)
- OllamaEmbeddings
- Multimodal RAG

### Data Processing

- unstructured (PDF partitioning)
- Pillow (image handling)

### Vector Store

- ChromaDB

### Frontend

- Streamlit

### Tools & Utilities

- UUID
- Base64 encoding
- OS / pathlib

---

## 📁 Project Structure

```text
teaching-assistant-chatbot/
│
├── ingestion.py        # PDF loading, partitioning, summarization
├── embeddings.py       # Calls ingestion, creates embeddings & vector store
├── rag_bot.py          # Multimodal RAG logic (text + image reasoning)
├── prompts.py          # Centralized prompt templates
├── streamlit_app.py    # UI for student interaction
│
├── data/
│   ├── pdfs/            # Input PDFs
│   └── images/          # Extracted images
│
├── chroma_db/           # Persistent vector store
├── requirements.txt
└── README.md
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- Ollama installed locally
- At least 8GB RAM (16GB recommended)

### Step-by-Step Setup

```bash
# Clone the repository
git clone https://github.com/saranyams057/Teaching_assistant_Chatbot/tree/master
cd teaching-assistant-chatbot
```

### Create virtual environment
```bash
python -m venv venv
```
### Activate virtual environment
### macOS/Linux:
```bash
source venv/bin/activate
```
### Windows:
```bash
venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Ollama Setup
```bash
ollama pull llava:7b
```

### Environment Variables

- Create a .env file:

- PDF_PATHS=data/book1.pdf,data/book2.pdf
- VECTOR_DIR=chroma_db

###  Run Embedding Pipeline (One-Time)
```bash
- python embeddings.py
```

### ⚡ Loads PDFs, summarizes text/tables/images, creates embeddings, stores in ChromaDB.
- ✅ Run only once unless new PDFs are added.

###  Launch Streamlit UI
```bash
- streamlit run streamlit_app.py
```


### 🌐 Open your browser at http://localhost:8501
- 📝 Ask questions based on PDFs and get text + image answers.

###  Querying / Using the RAG System

- Type your question in the Streamlit input box

- System retrieves relevant chunks from ChromaDB

- Ollama LLM generates an answer using multimodal reasoning

- Response may include:

- - Text explanation

- - Image references

## 💡 Example Question:
- “Explain photosynthesis based on the textbook content.”

## 🔄 Workflow / Pipeline Explanation

- PDF Ingestion

- Batch-wise loading of PDFs

- Extract text, tables, images

- Summarization Layer

- Reduces token size while preserving meaning

- Embedding & Storage

- Embeddings stored with metadata in ChromaDB

- Query-Time RAG

- Retrieve top-K chunks

- Separate reasoning for text/tables and images

- Merge final answer

## ⚡ Optimizations:

- Batch processing prevents memory overflow

- Cached summaries avoid repeated work

- Local LLM inference is fast and private

## ⚙️ Configuration

- Environment Variables:

- PDF_PATHS=data/book1.pdf,data/book2.pdf
- VECTOR_DIR=chroma_db


Config Files:

prompts.py → Centralized prompts for text/table/image reasoning

embeddings.py → Ingestion, summarization, embedding pipeline

rag_bot.py → Multimodal RAG logic for querying


## 🚀 Future Improvements

- Support for DOCX, EPUB textbooks

- GPU acceleration for faster embeddings and RAG inference

- Multi-language support


## 💡 Why This Design?

- Batch-wise PDF ingestion avoids memory issues

- Modality-specific reasoning keeps prompts clean

- Local LLM ensures privacy and no API costs

- ChromaDB persistence allows instant re-query

## 🤝 Contributing

Fork the repo

Create a feature branch

Submit a pull request

Follow PEP8 standards


