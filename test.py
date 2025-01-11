import aiohttp
import xml.etree.ElementTree as ET
import json

async def parse_rss_feed(rss_link):
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

# Example Usage
# You can use the function within an asyncio event loop
import asyncio

async def main():
    rss_link = "https://www.straitstimes.com/news/world/rss.xml"
    data = await parse_rss_feed(rss_link)
    print(data)
    # save the data to a json file
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

# Run the asynchronous main function
asyncio.run(main())
