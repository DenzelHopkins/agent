def up(db):
    """Creates the promises collection with schema validation.

    Args:
        db: The MongoDB database instance.
    """
    # Create collection with schema validator
    db.create_collection(
        "promises",
        validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["id", "promise", "source", "date"],
                "properties": {
                    "id":      {"bsonType": "string"},
                    "promise": {"bsonType": "string"},
                    "source":  {"bsonType": "string"},
                    "date":    {"bsonType": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
                },
                "additionalProperties": {"bsonType": ["string", "objectId"]},
            }
        },
    )
    # Enforce unique promise IDs
    db["promises"].create_index("id", unique=True)
