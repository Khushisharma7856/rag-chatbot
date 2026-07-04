from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader import papers


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


chunks = []


for paper in papers:

    paper_chunks = splitter.split_text(
        paper["text"]
    )

    for chunk in paper_chunks:

        chunks.append(
            {
                "id": paper["id"],
                "title": paper["title"],
                "authors": paper["authors"],
                "category": paper["category"],
                "text": chunk
            }
        )


print("Total chunks:", len(chunks))

print(chunks[0])