from sentence_transformers import CrossEncoder


reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, documents):

    pairs = []

    for doc in documents:
        pairs.append(
            [
                query,
                doc["text"]
            ]
        )


    scores = reranker.predict(pairs)


    results = []

    for doc, score in zip(documents, scores):

        results.append(
            {
                "document": doc,
                "score": float(score)
            }
        )


    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return results