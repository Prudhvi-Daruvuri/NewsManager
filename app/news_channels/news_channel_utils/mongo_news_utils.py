from ...mongo import MongoClient
from ...config import MongoConfig
from datetime import datetime



print("\nSetting up MongoDB connection...")
mongo_client = MongoClient.connect_to_mongo()
print("\nTesting get_database_list()...")
databases = MongoClient.get_database_list()
print(f"Available databases: {databases}")

print(f"News Database: {MongoConfig.NEWS_DATABASE}")

print(f"News Collection: {MongoConfig.NEWS_COLLECTION}")

# # Create News Database and Collection by inserting a document
# test_doc = {"title": "Test Document", "content": "Test Content", "created_at": datetime.utcnow()}
# doc_id = MongoClient.insert_document(MongoConfig.NEWS_DATABASE, MongoConfig.NEWS_COLLECTION, test_doc)
# print(f"Inserted document ID: {doc_id}")

# Get all the collections
collections = MongoClient.get_collection_list(MongoConfig.NEWS_DATABASE)
print(f"Collections in {MongoConfig.NEWS_DATABASE}: {collections}")


# -------------------------Deleting all records in collection--------------------------
# # Delete all the records in the collection by getting all the document ids using search_collection
# all_docs = MongoClient.search_collection(MongoConfig.NEWS_DATABASE, MongoConfig.NEWS_COLLECTION, {})

# for doc in all_docs:
#     doc_id = doc.get("id")
#     if doc_id:
#         print(f"Deleting document ID: {doc_id}")
#         MongoClient.delete_document(MongoConfig.NEWS_DATABASE, MongoConfig.NEWS_COLLECTION, str(doc_id))

# # Print the number of documents in the collection
# count = MongoClient.count_documents(MongoConfig.NEWS_DATABASE, MongoConfig.NEWS_COLLECTION, {})
# print(f"Number of documents in {MongoConfig.NEWS_DATABASE}.{MongoConfig.NEWS_COLLECTION}: {count}")
# -------------------------------------------------------------------------------------


# To run this file as a script:
# python -m app.news_channels.news_channel_utils.mongo_news_utils