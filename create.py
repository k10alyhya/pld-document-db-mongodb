"""CREATE: insert one document into the tracks collection."""
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from config import COLLECTION_NAME, DB_NAME, MONGO_URI

NEW_TRACK = {
    "_id": "demo_track_001",
    "name": "PLD Demo Song",
    "album": "PLD Demo Album",
    "artists": ["Demo Artist"],
    "popularity": 50,
    "duration_ms": 180000,
    "explicit": False,
    "audio_features": {"danceability": 0.5, "energy": 0.5},
    "label": "Holberton Records",  # extra field: other tracks don't have it
}


def main():
    tracks = MongoClient(MONGO_URI)[DB_NAME][COLLECTION_NAME]

    # MongoDB (mongosh):
    #   db.tracks.insertOne({ _id: "demo_track_001", name: "PLD Demo Song", ... })
    #
    # SQL:
    #   INSERT INTO tracks (id, name, album, popularity, duration_ms, explicit)
    #   VALUES ('demo_track_001', 'PLD Demo Song', 'PLD Demo Album', 50, 180000, FALSE);
    #   (artists and audio features would need extra INSERTs in other tables,
    #    and the "label" field would need ALTER TABLE first)
    try:
        result = tracks.insert_one(NEW_TRACK)
        print("Inserted document with _id:", result.inserted_id)
    except DuplicateKeyError:
        print("A document with this _id already exists.")


if __name__ == "__main__":
    main()
