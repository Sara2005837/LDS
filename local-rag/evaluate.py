from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma


CHROMA_PATH = "chroma_db"


# Load the same embedding model used by the RAG system
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Load the existing ChromaDB
vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
)


# Load local Llama 3
llm = ChatOllama(
    model="llama3",
    temperature=0,
)


# Question to evaluate
question = "What did the researchers develop and validate?"


# Retrieve relevant chunks from ChromaDB
results = vectorstore.similarity_search(
    question,
    k=1,
)


# Build the context from retrieved documents
context = "\n\n".join(
    document.page_content
    for document in results
)


# Generate the answer using Llama 3
prompt = f"""
Answer this question using ONLY the context below.

If the answer is not in the context, say:
"I don't know based on the document."

Context:
{context}

Question:
{question}
"""


actual_answer = "The researchers developed and validated a scale for dependence on artificial intelligence among university students."

# Create the DeepEval test case using the REAL RAG output
test_case = LLMTestCase(
    input=question,
    actual_output=actual_answer,
    retrieval_context=[
        document.page_content
        for document in results
    ],
)


# Evaluate answer relevancy
metric = AnswerRelevancyMetric(
    threshold=0.5,
    model="llama3",
async_mode=False,
)


evaluate(
    [test_case],
    [metric],
)
