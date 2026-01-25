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
- [Limitations & Known Issues](#limitations--known-issues)
- [Future Improvements](#future-improvements)
- [Why This Design?](#why-this-design)
- [Contributing](#contributing)
- [License](#license)

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

## ⚙️ Installation & Setup

### Prerequisites

Ensure the following are installed on your system:

- **Python 3.10+**
- **Ollama** (local LLM runtime)
- Minimum **8 GB RAM** (16 GB recommended for large PDFs)
- Git

---

### Step 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/teaching-assistant-chatbot.git
cd teaching-assistant-chatbot

### Step 2️⃣ Create and Activate Virtual Environment

Create a virtual environment to isolate dependencies:

```bash
python -m venv venv

### 4️⃣ Install Ollama

**Download and install Ollama** (required for the local `llava:7b` model):

- Visit [Ollama official website](https://ollama.com) and follow the installation instructions for your OS.

**Verify installation:**

```bash
ollama --version

### 5️⃣ Pull LLaVA Model

**Download the multimodal LLaVA model (`llava:7b`) for text, table, and image reasoning:**

```bash
ollama pull llava:7b

### 6️⃣ Add PDFs

**Place your textbooks (PDF files) in the `data/` directory:**

