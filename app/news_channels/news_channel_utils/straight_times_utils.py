"""
Utility functions for Straight Times news channel.
"""
import aiohttp
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from ..news_config import NEWS_CHANNELS
import json
import asyncio

# Get channel specific configuration
CHANNEL_CONFIG = NEWS_CHANNELS["straight_times"] if "straight_times" in NEWS_CHANNELS else None


async def parse_straight_times_opml_async(url):
    """
    Asynchronously fetches and parses an OPML file from the given URL,
    extracting specific fields into a dictionary.
    
    Args:
    - url (str): The URL of the OPML file.
    
    Returns:
    - dict: A dictionary with 'AllFeedDateModified' and a list of feeds with categories and rss links.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch data. HTTP Status Code: {response.status}")
            
            # Read and parse the XML content
            content = await response.text()
            root = ET.fromstring(content)
            
            # Extract the `dateModified` field
            date_modified = root.find("./head/dateModified").text
            
            # Extract category (text) and RSS link (xmlUrl) from the <outline> tags
            feeds = []
            for outline in root.findall("./body/outline"):
                category = outline.get("text")
                rss_link = outline.get("xmlUrl")
                feeds.append({"category": category, "rss_link": rss_link})
            
            # Construct the result dictionary
            result = {
                "AllFeedDateModified": date_modified,
                "feeds": feeds
            }
            return result

async def parse_rss_feed(rss_link):
    print(f" Parsing RSS Feed: {rss_link}")
    """
    Asynchronously fetches and parses an RSS feed, extracting lastBuildDate, pubDate,
    and details for each item.
    
    Args:
    - rss_link (str): The URL of the RSS feed.
    
    Returns:
    - dict: A dictionary containing lastBuildDate, pubDate, and a list of items with their details.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(rss_link) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch RSS feed. HTTP Status Code: {response.status}")
            
            # Parse the RSS content
            content = await response.text()
            root = ET.fromstring(content)
            
            # Extract channel-level metadata
            channel = root.find("channel")
            last_build_date = channel.find("lastBuildDate").text if channel.find("lastBuildDate") is not None else None
            pub_date = channel.find("pubDate").text if channel.find("pubDate") is not None else None
            
            # Extract all items
            items = []
            for item in channel.findall("item"):
                title = item.find("title").text if item.find("title") is not None else None
                link = item.find("link").text if item.find("link") is not None else None
                description = item.find("description").text if item.find("description") is not None else None
                guid = item.find("guid").text if item.find("guid") is not None else None
                guid_is_permalink = item.find("guid").get("isPermaLink") if item.find("guid") is not None else None
                item_pub_date = item.find("pubDate").text if item.find("pubDate") is not None else None
                source = item.find("source").text if item.find("source") is not None else None
                source_url = item.find("source").get("url") if item.find("source") is not None else None
                
                items.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "guid": guid,
                    "guid_is_permalink": guid_is_permalink,
                    "pubDate": item_pub_date,
                    "source": source,
                    "source_url": source_url
                })
            
            # Construct the result
            result = {
                "lastBuildDate": last_build_date,
                "pubDate": pub_date,
                "items": items
            }
            return result

async def fetch_rss_all_feeds() -> List[Dict[str, str]]:
    print(f" All Feeds URL: {CHANNEL_CONFIG['all_feeds_url']}")
    all_feeds_url = CHANNEL_CONFIG['all_feeds_url']
    result = await parse_straight_times_opml_async(all_feeds_url)
    # save the all feeds to a json
    # with open("all_feeds.json", "w") as f:
    #     json.dump(result, f, indent=4)
    # extract the list of feeds
    feeds = result.get("feeds", [])
    # for each feed, get the rss link, and parse the rss feed
    news_items = []
    rss_feeds = []
    for feed in feeds:
        category = feed.get("category")
        rss_link = feed.get("rss_link")
        # print(f"Category: {category}")
        # print(f"RSS Link: {rss_link}")
        if rss_link:
            rss_feed = await parse_rss_feed(rss_link)
            # Add the category to the feed
            rss_feed["category"] = category
            rss_feeds.append(rss_feed)

            # Gather all the news items from the feeds
            items = rss_feed.get("items", [])
            # Add the category to the items
            for item in items:
                item["category"] = category
                news_items.append(item)
    return news_items
    
    

async def main():
    rss_link = "https://www.straitstimes.com/news/world/rss.xml"
    data = await parse_rss_feed(rss_link)
    # save the data to a json file
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    asyncio.run(main())

    # To run this file as a script:
    # python -m app.news_channels.news_channel_utils.straight_times_utils