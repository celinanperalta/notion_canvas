from notion.client import NotionClient
import canvas_scraper as cs
import config as config

client = NotionClient(config.NOTION_TOKEN)
cv = client.get_collection_view(
    "https://www.notion.so/bf3147d28494406486d2670cf3812e5d?v=d44de919ca3746759f78c95bb568b4c0")


def get_all_rows():
    for row in cv.collection.get_rows():
        print(row.id)


def add_assignment(assignment):
    print("todo")


row = cv.collection.add_row()
row.name = "Just some data"
row.id = 100
result = cv.default_query().execute()
for row in result:
    print(row)
