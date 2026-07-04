import json


papers = []

with open("./data/arxiv.json", "r", encoding="utf-8") as f:

    for i, line in enumerate(f):

        if i == 1000:
            break

        paper = json.loads(line)

        doc = {
            "id": paper["id"],
            "title": paper["title"],
            "authors": paper["authors"],
            "text": paper["title"] + "\n\n" + paper["abstract"],
            "category": paper["categories"]
        }

        papers.append(doc)


print("Total papers:", len(papers))

print(papers[0])

