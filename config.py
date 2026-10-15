"""Shared settings for the PLD MongoDB project."""
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB", "pld_db")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "tracks")
DATA_FILE = os.getenv("DATA_FILE", "data/tracks.json")
