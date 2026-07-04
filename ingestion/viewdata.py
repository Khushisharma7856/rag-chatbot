import json


with open("./data/arxiv.json", "r", encoding="utf-8") as f:

    for i, line in enumerate(f):

        if i == 10:
            break

        paper = json.loads(line)

        print("\n--------------------")
        print("ID:", paper["id"])
        print("TITLE:", paper["title"])
        print("AUTHORS:", paper["authors"])
        print("CATEGORY:", paper["categories"])
        print("ABSTRACT:")
        print(paper["abstract"][:300])