"""UPDATE: change a field, change a nested field, append to an array."""
from pymongo import MongoClient

from config import COLLECTION_NAME, DB_NAME, MONGO_URI

TRACK_ID = "demo_track_001"


def main():
    tracks = MongoClient(MONGO_URI)[DB_NAME][COLLECTION_NAME]

    # 1) $set changes (or creates) a field
    # MongoDB (mongosh):
    #   db.tracks.updateOne({ _id: "demo_track_001" }, { $set: { popularity: 80 } })
    # SQL:
    #   UPDATE tracks SET popularity = 80 WHERE id = 'demo_track_001';
    tracks.update_one({"_id": TRACK_ID}, {"$set": {"popularity": 80}})

    # 2) $set on a nested field (dot notation)
    # MongoDB (mongosh):
    #   db.tracks.updateOne({ _id: "demo_track_001" },
    #                       { $set: { "audio_features.energy": 0.9 } })
    # SQL:
    #   UPDATE tracks SET energy = 0.9 WHERE id = 'demo_track_001';
    tracks.update_one({"_id": TRACK_ID}, {"$set": {"audio_features.energy": 0.9}})

    # 3) $push appends to an array (creates the array if it doesn't exist)
    # MongoDB (mongosh):
    #   db.tracks.updateOne({ _id: "demo_track_001" }, { $push: { genres: "pld" } })
    # SQL:
    #   INSERT INTO track_genres (track_id, genre) VALUES ('demo_track_001', 'pld');
    tracks.update_one({"_id": TRACK_ID}, {"$push": {"genres": "pld"}})

    print("After update:", tracks.find_one({"_id": TRACK_ID}))


if __name__ == "__main__":
    main()
