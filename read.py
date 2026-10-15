"""READ: query documents by _id, by array element and by nested field."""
from pymongo import MongoClient

from config import COLLECTION_NAME, DB_NAME, MONGO_URI


def main():
    tracks = MongoClient(MONGO_URI)[DB_NAME][COLLECTION_NAME]

    # 1) By _id
    # MongoDB (mongosh):
    #   db.tracks.findOne({ _id: "demo_track_001" })
    # SQL:
    #   SELECT * FROM tracks WHERE id = 'demo_track_001';
    print("By _id:", tracks.find_one({"_id": "demo_track_001"}))

    # 2) By array element ("artists" is an array)
    # MongoDB (mongosh):
    #   db.tracks.countDocuments({ artists: "Ingrid Michaelson" })
    # SQL:
    #   SELECT COUNT(*) FROM tracks t
    #   JOIN track_artists ta ON ta.track_id = t.id
    #   WHERE ta.artist = 'Ingrid Michaelson';
    count = tracks.count_documents({"artists": "Ingrid Michaelson"})
    print("Tracks by Ingrid Michaelson:", count)

    # 3) By nested field (dot notation reaches inside audio_features)
    # MongoDB (mongosh):
    #   db.tracks.find({ "audio_features.danceability": { $gt: 0.9 } },
    #                  { name: 1, "audio_features.danceability": 1, _id: 0 }).limit(3)
    # SQL:
    #   SELECT name, danceability FROM tracks
    #   WHERE danceability > 0.9 LIMIT 3;
    query = {"audio_features.danceability": {"$gt": 0.9}}
    projection = {"name": 1, "audio_features.danceability": 1, "_id": 0}
    print("Danceability > 0.9:")
    for track in tracks.find(query, projection).limit(3):
        print("  ", track)


if __name__ == "__main__":
    main()
