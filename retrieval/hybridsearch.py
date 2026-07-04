from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

from reranker import rerank
import ollama



# load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# connect elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "R4EJVf9QqMzzWjs9RNr1"),
    verify_certs=False
)



index_name = "arxiv_rag"



query = "Who is author of 'Calculation of prompt diphoton production cross sections at Tevatron and LHC energies'?"



# ---------------- VECTOR SEARCH ----------------

query_vector = model.encode(query).tolist()


vector_results = es.search(
    index=index_name,
    knn={
        "field": "embedding",
        "query_vector": query_vector,
        "k": 5,
        "num_candidates": 50
    }
)



# ---------------- BM25 SEARCH ----------------

keyword_results = es.search(
    index=index_name,
    query={
        "match": {
            "text": query
        }
    },
    size=5
)



# ---------------- COMBINE RESULTS ----------------

documents = []


for hit in vector_results["hits"]["hits"]:

    documents.append(
        hit["_source"]
    )



for hit in keyword_results["hits"]["hits"]:

    documents.append(
        hit["_source"]
    )



# remove duplicate papers

unique_documents = []

seen = set()


for doc in documents:

    if doc["id"] not in seen:

        unique_documents.append(doc)

        seen.add(doc["id"])




# ---------------- RERANK ----------------

reranked_results = rerank(
    query,
    unique_documents
)



print("\nTOP RETRIEVED DOCUMENTS\n")


for item in reranked_results[:3]:

    print("----------------------")

    print("Score:", item["score"])

    print("Title:", item["document"]["title"])

    print("Authors:", item["document"]["authors"])




# ---------------- SEND TO OLLAMA ----------------


context = ""


for item in reranked_results[:3]:
    doc = item["document"]
    context += (
        "Title: " + doc["title"] + "\n" +
        "Authors: " + doc["authors"] + "\n" +
        "Content: " + doc["text"] + "\n\n"
    )



response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": f"""
Answer the question using only the context below.

Context:
{context}

Question:
{query}
"""
        }
    ]
)


answer = response["message"]["content"]


print("\nFINAL ANSWER\n")

print(answer)