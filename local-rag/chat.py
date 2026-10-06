from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma


CHROMA_PATH = "chroma_db"


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
)

llm = ChatOllama(
    model="llama3",
    temperature=0,
)


print("Local RAG chatbot ready.")
print("Type 'exit' to quit.\n")


while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    print("\nSearching ChromaDB...")

    results = vectorstore.similarity_search(
        question,
        k=2,
    )

    print(f"Found {len(results)} relevant chunks.\n")

    for i, document in enumerate(results, 1):
        print(f"--- Retrieved chunk {i} ---")
        print(f"Source: {document.metadata.get('source')}")
        print(f"Page: {document.metadata.get('page')}")
        print(document.page_content[:1000])
        print()

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    prompt = f"""
Answer this question using ONLY the context below.

Keep your answer short: 2-3 sentences maximum.

If the answer is not in the context, say:
"I don't know based on the document."

Context:
{context}

Question:
{question}
"""

    print("Asking Llama 3...")

    response = llm.invoke(prompt)

    print("\nLlama:", response.content)
    print()
