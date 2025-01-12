from pymongo import MongoClient as PyMongoClient
from bson import ObjectId
from typing import List, Dict, Any, Optional, Union
from .config import Settings

class MongoClient:
    client: PyMongoClient = None

    @classmethod
    def connect_to_mongo(cls):
        """Connect to MongoDB."""
        cls.client = PyMongoClient(Settings.mongo.MONGODB_URL)

    @classmethod
    def close_mongo_connection(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()

    @classmethod
    def get_database_list(cls) -> List[str]:
        """Get list of all databases."""
        if not cls.client:
            raise ConnectionError("MongoDB client not connected")
        return cls.client.list_database_names()

    @classmethod
    def get_collection_list(cls, database: str) -> List[str]:
        """Get list of all collections in a database."""
        if not cls.client:
            raise ConnectionError("MongoDB client not connected")
        db = cls.client[database]
        return db.list_collection_names()

    @classmethod
    def get_document_by_id(cls, database: str, collection: str, doc_id: str) -> Optional[Dict]:
        """Get a document by its ID."""
        try:
            db = cls.client[database]
            coll = db[collection]
            document = coll.find_one({"_id": ObjectId(doc_id)})
            if document:
                document["id"] = str(document.pop("_id"))
                return document
            return None
        except Exception as e:
            print(f"Error getting document: {str(e)}")
            return None

    @classmethod
    def search_collection(
        cls,
        database: str,
        collection: str,
        query: Dict,
        projection: Dict = None,
        skip: int = 0,
        limit: int = 100,
        sort: List[tuple] = None
    ) -> List[Dict]:
        """
        Search documents in a collection.
        Args:
            database: Database name
            collection: Collection name
            query: MongoDB query dict
            projection: Fields to include/exclude
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            sort: List of (field, direction) tuples for sorting
        """
        try:
            db = cls.client[database]
            coll = db[collection]
            
            cursor = coll.find(query, projection)
            
            if sort:
                cursor = cursor.sort(sort)
            
            cursor = cursor.skip(skip).limit(limit)
            
            documents = []
            for doc in cursor:
                # doc["id"] = str(doc.pop("_id"))
                documents.append(doc)
            
            return documents
        except Exception as e:
            print(f"Error searching collection: {str(e)}")
            return []

    @classmethod
    def insert_document(
        cls,
        database: str,
        collection: str,
        document: Dict
    ) -> Optional[str]:
        """
        Insert a document into a collection.
        Returns the ID of the inserted document if successful.
        """
        try:
            db = cls.client[database]
            coll = db[collection]
            result = coll.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting document: {str(e)}")
            return None

    @classmethod
    def update_document(
        cls,
        database: str,
        collection: str,
        doc_id: str,
        update_data: Dict,
        upsert: bool = False
    ) -> bool:
        """Update a document by its ID."""
        try:
            db = cls.client[database]
            coll = db[collection]
            result = coll.update_one(
                {"_id": ObjectId(doc_id)},
                {"$set": update_data},
                upsert=upsert
            )
            return result.modified_count > 0 or (upsert and result.upserted_id)
        except Exception as e:
            print(f"Error updating document: {str(e)}")
            return False

    @classmethod
    def delete_document(
        cls,
        database: str,
        collection: str,
        doc_id: str
    ) -> bool:
        """Delete a document by its ID."""
        try:
            db = cls.client[database]
            coll = db[collection]
            result = coll.delete_one({"_id": ObjectId(doc_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {str(e)}")
            return False

    @classmethod
    def aggregate(
        cls,
        database: str,
        collection: str,
        pipeline: List[Dict]
    ) -> List[Dict]:
        """
        Perform an aggregation pipeline operation.
        Args:
            database: Database name
            collection: Collection name
            pipeline: List of aggregation pipeline stages
        """
        try:
            db = cls.client[database]
            coll = db[collection]
            documents = []
            for doc in coll.aggregate(pipeline):
                if "_id" in doc:
                    doc["id"] = str(doc.pop("_id"))
                documents.append(doc)
            return documents
        except Exception as e:
            print(f"Error in aggregation: {str(e)}")
            return []

    @classmethod
    def count_documents(
        cls,
        database: str,
        collection: str,
        query: Dict = {}
    ) -> int:
        """Count documents in a collection matching the query."""
        try:
            db = cls.client[database]
            coll = db[collection]
            return coll.count_documents(query)
        except Exception as e:
            print(f"Error counting documents: {str(e)}")
            return 0

    @classmethod
    def create_index(
        cls,
        database: str,
        collection: str,
        keys: Union[str, List[tuple]],
        unique: bool = False
    ) -> str:
        """
        Create an index on a collection.
        Args:
            database: Database name
            collection: Collection name
            keys: Either a single key name or list of (key, direction) tuples
            unique: Whether the index should be unique
        """
        try:
            db = cls.client[database]
            coll = db[collection]
            return coll.create_index(keys, unique=unique)
        except Exception as e:
            print(f"Error creating index: {str(e)}")
            return None
