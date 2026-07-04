from sentence_transformers import SentenceTransformer
from chunker import chunks


# load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


embedded_chunks = []


for chunk in chunks:

    vector = model.encode(
        chunk["text"]
    )

    embedded_chunks.append(
        {
            **chunk,
            "embedding": vector.tolist()
        }
    )


print("Embedded chunks:", len(embedded_chunks))

print(
    len(embedded_chunks[0]["embedding"])
)