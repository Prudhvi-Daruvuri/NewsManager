import os
from scrapegraphai.graphs import SmartScraperGraph
import json
from .crawler_config import prompt, graph_config
import asyncio

async def smart_news_crawler(source_link, prompt=prompt, graph_config=graph_config):
    # Create the SmartScraperGraph instance
    smart_scraper_graph = SmartScraperGraph(
        prompt=prompt,
        source=source_link,
        config=graph_config
    )

    # Run the pipeline (ensure async execution is handled properly)
    result = await asyncio.to_thread(smart_scraper_graph.run)

    # Save the result to a JSON file
    with open("result.json", "w") as f:
        json.dump(result, f, indent=4)

    return result

async def main():
    source_link = "https://www.straitstimes.com/world/europe/trumps-ukraine-envoy-keith-kellogg-attends-iran-opposition-event-in-paris"
    result = await smart_news_crawler(source_link)
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    asyncio.run(main())

# To run this file as a script:
# python -m app.crawler.crawler_utils