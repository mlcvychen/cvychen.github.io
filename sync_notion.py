import os
import requests

# 从环境变量获取
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

if not NOTION_TOKEN or not DATABASE_ID:
    raise ValueError("请确保环境变量 NOTION_TOKEN 和 NOTION_DATABASE_ID 已配置")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 查询数据库
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
response = requests.post(url, headers=HEADERS)
data = response.json()

# 打印返回结果方便调试
print("调试信息：数据库返回内容")
print(data)

# 创建 posts 文件夹
os.makedirs("posts", exist_ok=True)

# 遍历每一条笔记
for page in data.get("results", []):
    properties = page.get("properties", {})

    # 获取标题字段（根据你的数据库字段名修改）
    title_field = properties.get("Name")  # 注意字段名必须和 Notion 数据库一致
    if not title_field:
        print("⚠️ 找不到标题字段，跳过")
        continue

    title = title_field["title"][0]["plain_text"] if title_field["title"] else "无标题"

    # 获取正文内容（假设正文字段叫 "Content"）
    content_md = f"# {title}\n\n"
    content_field = properties.get("Content")
    if content_field and content_field.get("rich_text"):
        for block in content_field["rich_text"]:
            content_md += block.get("plain_text", "") + "\n\n"
    else:
        content_md += "(正文为空)\n\n"

    # 文件名安全处理
    safe_title = "".join(c if c.isalnum() or c in "_-" else "_" for c in title)
    filename = f"posts/{safe_title}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content_md)

    print(f"✅ 同步成功: {filename}")

print("🎉 所有笔记同步完成！")
