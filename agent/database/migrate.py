import importlib
import os
from pathlib import Path

from pymongo import MongoClient

_CLIENT = MongoClient(os.environ["MONGO_URL"])
_DB = _CLIENT["agent"]
_MIGRATIONS_COLLECTION = "_migrations"


def run():
    """Applies all pending migrations in order."""
    applied = {
        doc["name"]
        for doc in _DB[_MIGRATIONS_COLLECTION].find({}, {"name": 1})
    }

    migration_files = sorted(
        Path(__file__).parent.glob("migrations/[0-9]*.py"))

    for path in migration_files:
        name = path.stem
        if name in applied:
            continue
        module = importlib.import_module(f"database.migrations.{name}")
        module.up(_DB)
        _DB[_MIGRATIONS_COLLECTION].insert_one({"name": name})
        print(f"Applied migration: {name}")
