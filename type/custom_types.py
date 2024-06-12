from pydantic import BaseModel, Field, validator
from firebase_admin import credentials, firestore
from typing import Any

class FirestoreServerTimestamp:
    """Custom type to represent Firestore's SERVER_TIMESTAMP."""
    pass

def is_firestore_server_timestamp(value: Any) -> bool:
    return value == firestore.SERVER_TIMESTAMP
