from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


DOCUMENTS_PATH = Path("documents")
CHROMA_PATH = "chroma_db"


print("Loading PDF documents...")

all_documents = []

for pdf_file in DOCUMENTS_PATH.glob("*.pdf"):
    print(f"Loading: {pdf_file.name}")

    loader = PyPDFLoader(str(pdf_file))
    documents = loader.load()

    for document in documents:
        document.metadata["source"] = pdf_file.name

    all_documents.extend(documents)

print(f"\nLoaded {len(all_documents)} pages in total.")


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(all_documents)

print(f"Created {len(chunks)} chunks.")


print("\nCreating embeddings with nomic-embed-text...")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


print("Creating ChromaDB database...")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_PATH,
)

print("\nDone!")
print(f"ChromaDB stored in: {CHROMA_PATH}")