📘 Teaching Assistant Chatbot (Multimodal RAG)

A local, multimodal Retrieval-Augmented Generation (RAG) chatbot that acts as a school teaching assistant, capable of answering questions from large textbook PDFs containing text, tables, and images—fully offline using Ollama + LLaVA.

📑 Table of Contents

Overview

Key Features

Architecture & Design

Tech Stack

Project Structure

Installation & Setup

Usage

Workflow / Pipeline Explanation

Configuration

Limitations & Known Issues

Future Improvements

Why This Design?

Contributing

License

📖 Overview

This project is a Teaching Assistant Chatbot built using a multimodal RAG architecture.

It allows students to ask questions from real school textbooks (PDFs with 800+ pages) and receive accurate answers derived from:

Text explanations

Tables

Diagrams and images

Real-World Use Case

Digital classroom assistant

Self-study companion for students

Offline AI tutor for schools with limited internet access

Why This Is Non-Trivial

Handles very large PDFs

Supports multimodal reasoning

Runs entirely locally (no APIs)

Memory-efficient ingestion and retrieval

✨ Key Features

📚 Supports multiple large PDFs

🧠 Multimodal RAG (Text + Tables + Images)

⚡ Memory-efficient, page-wise ingestion

🗂 Persistent vector store (ChromaDB)

🔍 Context-aware retrieval (Top-K)

🖼 Image reasoning via LLaVA

🔐 Fully offline & privacy-safe

🧩 Modular, production-ready design

🏗 Architecture & Design
System Flow

PDFs are loaded page-by-page

Content is split into:

Text

Tables

Images

Each modality is summarized

Summaries are embedded

Vectors are stored in ChromaDB

User query retrieves relevant chunks

LLaVA reasons over:

Text & tables

Images (if relevant)

Final answer is generated

Why This Architecture?

Avoids loading entire PDFs into memory

Summarization reduces token cost

Multimodal RAG reflects real textbooks

Local-first for cost and privacy

🧰 Tech Stack
Backend

Python

LangChain

AI / ML

Ollama

LLaVA (7B)

OllamaEmbeddings

Document Processing

Unstructured (partition_pdf)

Vector Store

ChromaDB

Frontend

Streamlit

Tools

dotenv

uuid

base64

📂 Project Structure
.
├── ingestion.py          # PDF loading, parsing & summarization
├── embeddings.py         # Embedding + vector store creation
├── rag.py                # Multimodal RAG logic
├── prompts.py            # Centralized prompt templates
├── streamlit_app.py      # UI for chatbot
├── data/
│   ├── book1.pdf
│   ├── book2.pdf
│   └── images/           # Extracted images
├── chroma_db/            # Persistent vector store
├── requirements.txt
└── README.md

⚙️ Installation & Setup
Prerequisites

Python 3.10+

Ollama installed locally

Minimum 8 GB RAM (16 GB recommended)

Git

Step 1️⃣ Clone the Repository
git clone https://github.com/your-org/teaching-assistant-chatbot.git
cd teaching-assistant-chatbot

Step 2️⃣ Create & Activate Virtual Environment
python -m venv venv


Linux / macOS

source venv/bin/activate


Windows

venv\Scripts\activate

Step 3️⃣ Install Dependencies
pip install -r requirements.txt


No API keys required.

Step 4️⃣ Install Ollama

Download and install from:
https://ollama.com

Step 5️⃣ Pull Required Model
ollama pull llava:7b

▶️ Usage
Step 1️⃣ Add PDFs

Place PDFs in:

data/
 ├── book1.pdf
 └── book2.pdf

Step 2️⃣ Run Embedding Pipeline
python embeddings.py


This step:

Extracts content

Summarizes

Embeds

Stores vectors permanently

Run only once unless PDFs change.

Step 3️⃣ Start the Chatbot UI
streamlit run streamlit_app.py


Open browser:

http://localhost:8501

Sample Input
Explain the process of photosynthesis using the diagram.

Sample Output

Clear explanation from textbook text

Additional insights from diagrams (if available)

🔄 Workflow / Pipeline Explanation
PDFs
 ↓
Page-wise Loading
 ↓
Text / Table / Image Separation
 ↓
Summarization
 ↓
Embedding
 ↓
ChromaDB
 ↓
Retriever
 ↓
Multimodal Prompting
 ↓
LLaVA Reasoning
 ↓
Answer

🔧 Configuration
Configurable Values

TOP_K – number of retrieved chunks

COLLECTION_NAME

VECTOR_DIR

Ollama model (llava:7b)

Defined directly in code.

⚠️ Limitations & Known Issues

OCR quality depends on PDF scans

Image reasoning accuracy varies

No page citation yet

Initial ingestion may take time

🚀 Future Improvements

Source/page references

Hybrid retrieval (BM25 + Vector)

Docker support

Advanced OCR

Chat history memory

Better UI annotations

🤔 Why This Design?
Decision	Reason
Local LLM	Privacy & zero cost
Summarize before embedding	Performance & recall
Multimodal RAG	Real textbook understanding
ChromaDB	Lightweight & persistent
🤝 Contributing

Fork the repo

Create a feature branch

Commit clean code

Open a Pull Request
