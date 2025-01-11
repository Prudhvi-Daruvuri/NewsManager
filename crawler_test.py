import os
from scrapegraphai.graphs import SmartScraperGraph
import json


# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
        "api_key": "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",
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": True,
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="""Extract All the news information from the news page. Extract the 
                1. title, 
                2. author, 
                3. date, 
                4. article, 
                5. category, 
                6. keywords, 
                7. image_links, 
                8. video_links, 
                9. related_news_links.
                Extract information only if the information is present in the page. If the information is not present in the page, return 'NA' for that field.
                
                Generate these additional fields based on the extracted information:
                1. sentiment (positive, negative, neutral),
                2. summary ( should be a list of precise bullet points, each bullet point should be less than 100 words),
                3. explained_summary (should be a text summary, with history and context so that a new reader can understand the context of the news),
                4. importance_rating (1-10, where 10 is a breaking news and 1 is not important).
                """,
    source="https://www.straitstimes.com/world/europe/trumps-ukraine-envoy-keith-kellogg-attends-iran-opposition-event-in-paris",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()
# print(json.dumps(result, indent=4))

# Save the result to a JSON file
with open("result.json", "w") as f:
    json.dump(result, f, indent=4)
