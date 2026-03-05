import json
import os

from langchain_core.tools import tool
from pymongo import MongoClient

_CLIENT = MongoClient(os.environ["MONGO_URL"])


@tool
def mongo_list() -> str:
    """List all databases and their collections in MongoDB."""
    try:
        result = {}
        for db_name in _CLIENT.list_database_names():
            if db_name in ("admin", "config", "local"):
                continue
            result[db_name] = _CLIENT[db_name].list_collection_names()
        return json.dumps(result) if result else "No user databases found."
    except Exception as e:
        return f"Database error: {e}"


@tool
def mongo_find(database: str, collection: str, query: str) -> str:
    """Query documents from a MongoDB collection.

    Args:
        database: The MongoDB database name.
        collection: The collection to query.
        query: A JSON string representing the MongoDB filter (e.g. '{"name": "Alice"}').
    """
    try:
        filter_dict = json.loads(query)
    except json.JSONDecodeError as e:
        return f"Invalid query JSON: {e}"

    try:
        docs = list(_CLIENT[database][collection].find(filter_dict, {"_id": 0}, limit=10))
    except Exception as e:
        return f"Database error: {e}"

    if not docs:
        return "No documents found."
    return json.dumps(docs, default=str)


@tool
def mongo_insert(database: str, collection: str, document: str) -> str:
    """Insert a document into a MongoDB collection.

    Args:
        database: The MongoDB database name.
        collection: The collection to insert into.
        document: A JSON string representing the document to insert.
    """
    try:
        doc_dict = json.loads(document)
    except json.JSONDecodeError as e:
        return f"Invalid document JSON: {e}"

    try:
        result = _CLIENT[database][collection].insert_one(doc_dict)
    except Exception as e:
        return f"Database error: {e}"

    return f"Inserted document with id: {result.inserted_id}"
