import os
import uuid
from typing import Annotated

from langchain_core.tools import tool
from pymongo import MongoClient

from models import Promise
from utils import get_logger

# Module logger
logger = get_logger(__name__)

# Connect to MongoDB
_client = MongoClient(os.environ["MONGO_URL"])
# Target promises collection
_collection = _client["agent"]["promises"]


@tool
def save_promises(promises: Annotated[list[Promise], "List of promises to save"]) -> str:
    """Save a list of promises to the database.

    Args:
        promises: List of promises, each with promise, source, and date fields.
    """
    for p in promises:
        # Serialize promise to dict
        doc = p.model_dump()
        # Assign unique ID
        doc["id"] = str(uuid.uuid4())
        # Insert into collection
        _collection.insert_one(doc)
        logger.info("Inserted promise id=%s source=%s date=%s",
                    doc["id"], doc["source"], doc["date"])
    return f"Saved {len(promises)} promises."
