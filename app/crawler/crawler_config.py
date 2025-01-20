# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
        "api_key": "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",
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": True,
}

prompt="""Extract All the news information from the news page. Extract the 
                1. title, 
                2. author, 
                3. date, 
                4. article, 
                5. keywords, 
                6. image_links, 
                7. video_links, 
                8. related_news_links.
                Extract information only if the information is present in the page. If the information is not present in the page, return 'NA' for that field.
                
                Generate these additional fields based on the extracted information:
                1. sentiment (positive, negative, neutral),
                2. summary ( should be a list of precise bullet points, each bullet point should be less than 100 words),
                3. explained_summary (should be a text summary, with history and context so that a new reader can understand the context of the news),
                4. importance_rating (1-10, where 10 is a breaking news and 1 is not important).
                """
