import sys
import os
from datetime import datetime
from contextlib import contextmanager

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.mongo import MongoClient

# Test database and collection names
TEST_DB = "test_database"
TEST_COLLECTION = "test_collection"

@contextmanager
def mongo_test_context():
    """Context manager for MongoDB connection in tests"""
    try:
        # Setup: Connect to MongoDB
        print("\nSetting up MongoDB connection...")
        MongoClient.connect_to_mongo()
        yield
    finally:
        # Cleanup: Drop test database and close connection
        print("\nCleaning up...")
        if MongoClient.client:
            MongoClient.client.drop_database(TEST_DB)
            MongoClient.close_mongo_connection()
        print("Test database dropped and connection closed")

# Main test execution
with mongo_test_context():
    # Test 1: List Databases
    print("\nTesting get_database_list()...")
    databases = MongoClient.get_database_list()
    print(f"Available databases: {databases}")

    # Test 2: Create and List Collections
    print("\nTesting collection operations...")
    test_doc = {"test_field": "test_value", "created_at": datetime.utcnow()}
    MongoClient.insert_document(TEST_DB, TEST_COLLECTION, test_doc)
    collections = MongoClient.get_collection_list(TEST_DB)
    print(f"Collections in {TEST_DB}: {collections}")

    # Test 3: Insert Document
    print("\nTesting insert_document()...")
    new_doc = {
        "title": "Test Document",
        "content": "Test Content",
        "created_at": datetime.utcnow()
    }
    doc_id = MongoClient.insert_document(TEST_DB, TEST_COLLECTION, new_doc)
    print(f"Inserted document ID: {doc_id}")

    # Test 4: Get Document by ID
    print("\nTesting get_document_by_id()...")
    retrieved_doc = MongoClient.get_document_by_id(TEST_DB, TEST_COLLECTION, doc_id)
    print(f"Retrieved document: {retrieved_doc}")

    # Test 5: Update Document
    print("\nTesting update_document()...")
    update_data = {"title": "Updated Title"}
    update_success = MongoClient.update_document(TEST_DB, TEST_COLLECTION, doc_id, update_data)
    updated_doc = MongoClient.get_document_by_id(TEST_DB, TEST_COLLECTION, doc_id)
    print(f"Updated document: {updated_doc}")

    # Test 6: Search Documents
    print("\nTesting search_collection()...")
    # Insert more documents for search test
    docs = [
        {"type": "A", "value": 1},
        {"type": "A", "value": 2},
        {"type": "B", "value": 3}
    ]
    for doc in docs:
        MongoClient.insert_document(TEST_DB, TEST_COLLECTION, doc)

    results = MongoClient.search_collection(
        TEST_DB,
        TEST_COLLECTION,
        query={"type": "A"},
        sort=[("value", 1)]
    )
    print(f"Search results: {results}")

    # Test 7: Count Documents
    print("\nTesting count_documents()...")
    count = MongoClient.count_documents(TEST_DB, TEST_COLLECTION, {"type": "A"})
    print(f"Count of documents with type 'A': {count}")

    # Test 8: Aggregation
    print("\nTesting aggregate()...")
    pipeline = [
        {"$match": {"type": "A"}},
        {"$group": {"_id": "$type", "total": {"$sum": "$value"}}}
    ]
    agg_results = MongoClient.aggregate(TEST_DB, TEST_COLLECTION, pipeline)
    print(f"Aggregation results: {agg_results}")

    # Test 9: Create Index
    print("\nTesting create_index()...")
    index_name = MongoClient.create_index(
        TEST_DB,
        TEST_COLLECTION,
        [("type", 1), ("value", -1)],
        unique=True
    )
    print(f"Created index: {index_name}")

    # Test 10: Test Unique Index
    print("\nTesting unique index constraint...")
    doc1 = {"type": "C", "value": 1}
    doc2 = {"type": "C", "value": 1}
    doc1_id = MongoClient.insert_document(TEST_DB, TEST_COLLECTION, doc1)
    duplicate_id = MongoClient.insert_document(TEST_DB, TEST_COLLECTION, doc2)
    print(f"Duplicate document insert result: {duplicate_id} (should be None)")

    # Get all the collections
    collections = MongoClient.get_collection_list(TEST_DB)
    print(f"Collections in {TEST_DB}: {collections}")

    
    # Test 11: Delete Document
    print("\nTesting delete_document()...")
    delete_success = MongoClient.delete_document(TEST_DB, TEST_COLLECTION, doc_id)
    deleted_doc = MongoClient.get_document_by_id(TEST_DB, TEST_COLLECTION, doc_id)
    print(f"Delete success: {delete_success}")
    print(f"Deleted document retrieval (should be None): {deleted_doc}")
