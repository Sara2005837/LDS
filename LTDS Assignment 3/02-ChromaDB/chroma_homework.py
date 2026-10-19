
import chromadb


client = chromadb.PersistentClient(path="./chroma_data")


collection = client.get_or_create_collection(
    name="homework_demo"
)


collection.add(
    ids=["1", "2", "3"],
    documents=[
        "Albania is a small country",
        "Dogs enjoy going for walks",
        "Python is a programming language"
    ],
    embeddings=[
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
        [0.0, 0.0, 1.0]
    ]
)

results = collection.query(
    query_embeddings=[[0.95, 0.05, 0.0]],
    n_results=2
)

print("Top 2 matching documents:")
for document in results["documents"][0]:
    print("-", document)
