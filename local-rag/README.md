# Local PDF RAG System

This project implements a local Retrieval-Augmented Generation (RAG) system for
question answering over PDF documents.

The system is based on LangChain, Ollama, Llama 3, ChromaDB, local embeddings,
and DeepEval.

## Technologies

- Python
- LangChain
- Ollama
- Llama 3
- ChromaDB
- nomic-embed-text
- PyPDF
- DeepEval

## RAG Pipeline

PDF documents
→ text extraction
→ text chunking
→ local embeddings
→ ChromaDB
→ similarity search
→ relevant context
→ Llama 3
→ generated answer

## Project Files

- `ingest.py` - loads PDF documents, splits them into chunks, creates embeddings,
  and stores them in ChromaDB.
- `chat.py` - runs the local RAG chatbot.
- `evaluate.py` - evaluates answer relevancy using DeepEval and local Ollama/Llama 3.
- `documents/` - folder for PDF documents.
- `requirements.txt` - Python dependencies.
- `.gitignore` - files and folders excluded from GitHub.

## Requirements

- macOS or another compatible operating system
- Python 3.12
- Ollama
- Llama 3
- nomic-embed-text

## Ollama Models

The project uses:

```text
llama3
nomic-embed-text
