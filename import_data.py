"""Load data/tracks.json into MongoDB.

The collection is dropped first, so the script is safe to run many times.

Usage:
    python import_data.py
"""
import json
import sys
from pathlib import Path

from pymongo import MongoClient

from config import COLLECTION_NAME, DATA_FILE, DB_NAME, MONGO_URI

BATCH_SIZE = 5000  # documents sent to MongoDB per insert_many call


def load_tracks(path):
    """Read the JSON file and return a list of track documents."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def import_tracks(collection, tracks):
    """Replace the collection content with `tracks`, inserting in batches."""
    collection.drop()
    for start in range(0, len(tracks), BATCH_SIZE):
        collection.insert_many(tracks[start:start + BATCH_SIZE])
    return collection.count_documents({})


def main():
    if not Path(DATA_FILE).is_file():
        sys.exit(f"Data file not found: {DATA_FILE}\n"
                 "Place tracks.json inside the data/ folder.")

    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME]

    tracks = load_tracks(DATA_FILE)
    total = import_tracks(collection, tracks)
    print(f"Imported {total} documents into {DB_NAME}.{COLLECTION_NAME}")


if __name__ == "__main__":
    main()
