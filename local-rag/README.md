# Local PDF RAG System

This project implements a local Retrieval-Augmented Generation (RAG) system for question answering over PDF documents.

The system is based on LangChain, Ollama, Llama 3, ChromaDB, local embeddings, and DeepEval.

## Technologies

* Python
* LangChain
* Ollama
* Llama 3
* ChromaDB
* nomic-embed-text
* PyPDF
* DeepEval

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

* `ingest.py` - loads PDF documents, splits them into chunks, creates embeddings, and stores them in ChromaDB.
* `chat.py` - runs the local RAG chatbot.
* `evaluate.py` - evaluates RAG answers using DeepEval and the local Ollama/Llama 3 model.
* `documents/` - folder for PDF documents.
* `requirements.txt` - Python dependencies.
* `.gitignore` - files and folders excluded from GitHub.

## Requirements

* macOS or another compatible operating system
* Python 3.12
* Ollama
* Llama 3
* nomic-embed-text

## Ollama Models

The project uses:

```text
llama3
nomic-embed-text
```

Install/download these models through Ollama before running the project.

## Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Add Documents

Place PDF files inside:

```text
documents/
```

Then build the ChromaDB vector database:

```bash
python3 ingest.py
```

## Run the RAG Chatbot

```bash
python3 chat.py
```

The chatbot retrieves relevant passages from the PDFs and asks Llama 3 to answer using the retrieved context.

## Evaluation

DeepEval is configured to evaluate the RAG system using the local Ollama Llama 3 model rather than a paid external API.

Configure DeepEval:

```bash
deepeval set-ollama --model=llama3 --base-url="http://localhost:11434"
export LOCAL_MODEL_API_KEY=ollama
```

Then run:

```bash
python3 evaluate.py
```

### Evaluation Note

The DeepEval evaluation requires Llama 3 to generate an evaluation judgment locally. On slower hardware, this evaluation step may take a long time or reach DeepEval's timeout before completing.

The RAG system itself runs locally, and the DeepEval configuration is included to demonstrate evaluation using Ollama rather than a paid external API.

## Notes

The ChromaDB database and Python virtual environment are generated locally and are excluded from the GitHub repository.

PDF documents may also be excluded from the repository where redistribution rights do not permit uploading the files.

