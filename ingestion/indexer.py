from embedder import embedded_chunks
from elasticsearch import Elasticsearch


es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "R4EJVf9QqMzzWjs9RNr1"),
    verify_certs=False
)



index_name = "arxiv_rag"


if not es.indices.exists(index=index_name):

    es.indices.create(
        index=index_name,
        mappings={
            "properties": {

                "text": {
                    "type": "text"
                },

                "title": {
                    "type": "text"
                },

                "authors": {
                    "type": "text"
                },

                "category": {
                    "type": "keyword"
                },

                "embedding": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    )


for chunk in embedded_chunks:

    es.index(
        index=index_name,
        document=chunk
    )


print("All chunks stored!")