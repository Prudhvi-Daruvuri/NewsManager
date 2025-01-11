"""
Straight Times news channel implementation.
"""
from typing import List, Dict, Any
from .news_config import NEWS_CHANNELS
from .news_channel_utils import straight_times_utils
import json

# Get channel specific configuration
CHANNEL_CONFIG = NEWS_CHANNELS["straight_times"] if "straight_times" in NEWS_CHANNELS else None

async def update_news() -> None:
    """
    Update news from Straight Times.
    """
    # Access config using CHANNEL_CONFIG

    pass

async def extract_news() -> List[Dict[str, Any]]:
    """
    Extract news from Straight Times.
    """
    # Access config using CHANNEL_CONFIG
    all_news_items = await straight_times_utils.fetch_rss_all_feeds()
    # save the news items to a json
    with open("news_items.json", "w") as f:
        json.dump(all_news_items, f, indent=4)
    # print(fetch_rss_all_feeds)
    pass

if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("Testing Straight Times News Channel")
        print("-" * 40)
        
        if CHANNEL_CONFIG is None:
            print("Warning: Channel configuration not found!")
        else:
            print(f"Channel Name: {CHANNEL_CONFIG['name']}")
        
        # print("\nTesting update_news()...")
        # await update_news()
        
        print("\nTesting extract_news()...")
        news = await extract_news()
        print(f"Retrieved news: {news}")

    # Run the async main function
    asyncio.run(main())

    # python -m app.news_channels.straight_times
