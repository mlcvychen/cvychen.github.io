import os
import requests
import json

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

res = requests.post(url, headers=headers)
data = res.json()

# 遍历笔记
for page in data["results"]:
    title = page["properties"]["Name"]["title"][0]["plain_text"]
    content = f"# {title}\n\n(这里可以扩展获取更多内容)"
    filename = f"posts/{title.replace(' ', '_')}.md"
    os.makedirs("posts", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Notion 同步完成！")
