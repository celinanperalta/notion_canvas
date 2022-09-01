from notion_client import Client
import canvas_scraper as cs
import config as config

client = Client(auth=config.NOTION_TOKEN)

notion_db = client.databases.query(**{
    "database_id": config.NOTION_LINK
})

def get_existing_rows():
    results = client.databases.query(
    **{
        "database_id": config.NOTION_LINK,
    }
    ).get("results")
    return [x['properties']['Assignment ID']['number'] for x in results]

