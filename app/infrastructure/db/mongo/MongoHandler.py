from loguru import logger
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Any, Dict, List, Optional, Tuple, Union


class MongoHandler:
    def __init__(self, url: str, db_name: str, **kwargs):
        try:
            self.client = MongoClient(url, **kwargs)
            self.db = self.client[db_name]
            logger.info(f"✅ Connected to MongoDB: {url} / {db_name}")
        except Exception as e:
            logger.exception(f"❌ Failed to connect to MongoDB: {e}")
            raise

    def close(self):
        self.client.close()
        logger.info("🛑 MongoDB connection closed.")

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        try:
            result = self.get_collection(collection_name).insert_one(document)
            logger.info(f"Inserted one into {collection_name}, ID: {result.inserted_id}")
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.exception(f"Insert one failed: {e}")
            return None

    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        try:
            result = self.get_collection(collection_name).insert_many(documents)
            logger.info(f"Inserted {len(result.inserted_ids)} documents into {collection_name}")
            return [str(_id) for _id in result.inserted_ids]
        except PyMongoError as e:
            logger.exception(f"Insert many failed: {e}")
            return []

    def find_one(self, collection_name: str, query: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        try:
            query = query or {}
            result = self.get_collection(collection_name).find_one(query)
            logger.debug(f"find_one result: {result}")
            return result
        except PyMongoError as e:
            logger.exception(f"Find one failed: {e}")
            return None

    def find_many(
        self,
        collection_name: str,
        query: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[Tuple[str, int]]] = None
    ) -> List[Dict[str, Any]]:
        try:
            query = query or {}
            cursor = self.get_collection(collection_name).find(query).skip(skip).limit(limit)
            if sort:
                cursor = cursor.sort(sort)
            results = list(cursor)
            logger.debug(f"find_many returned {len(results)} documents")
            return results
        except PyMongoError as e:
            logger.exception(f"Find many failed: {e}")
            return []

    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        try:
            result = self.get_collection(collection_name).update_one(query, {"$set": update})
            logger.info(f"Updated {result.modified_count} document(s) in {collection_name}")
            return result.modified_count
        except PyMongoError as e:
            logger.exception(f"Update one failed: {e}")
            return 0

    def update_many(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        try:
            result = self.get_collection(collection_name).update_many(query, {"$set": update})
            logger.info(f"Updated {result.modified_count} document(s) in {collection_name}")
            return result.modified_count
        except PyMongoError as e:
            logger.exception(f"Update many failed: {e}")
            return 0

    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
        try:
            result = self.get_collection(collection_name).delete_one(query)
            logger.info(f"Deleted {result.deleted_count} document(s) from {collection_name}")
            return result.deleted_count
        except PyMongoError as e:
            logger.exception(f"Delete one failed: {e}")
            return 0

    def delete_many(self, collection_name: str, query: Dict[str, Any]) -> int:
        try:
            result = self.get_collection(collection_name).delete_many(query)
            logger.info(f"Deleted {result.deleted_count} documents from {collection_name}")
            return result.deleted_count
        except PyMongoError as e:
            logger.exception(f"Delete many failed: {e}")
            return 0

    def create_index(
        self,
        collection_name: str,
        keys: Union[str, List[Tuple[str, int]]],
        unique: bool = False,
        **kwargs
    ) -> str:
        try:
            if isinstance(keys, str):
                keys = [(keys, 1)]
            index_name = self.get_collection(collection_name).create_index(keys, unique=unique, **kwargs)
            logger.info(f"Created index on {collection_name}: {index_name}")
            return index_name
        except PyMongoError as e:
            logger.exception(f"Create index failed: {e}")
            return ""

if __name__ == "__main__":
    mongo_handler = MongoHandler(url="mongodb+srv://root:wzpace3158@king.aniol8r.mongodb.net/?retryWrites=true&w=majority&appName=king", db_name="king")
    print(mongo_handler.get_collection("equipments"))
