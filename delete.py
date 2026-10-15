"""DELETE: remove one document and check the others are untouched."""
from pymongo import MongoClient

from config import COLLECTION_NAME, DB_NAME, MONGO_URI

TRACK_ID = "demo_track_001"


def main():
    tracks = MongoClient(MONGO_URI)[DB_NAME][COLLECTION_NAME]

    before = tracks.count_documents({})

    # MongoDB (mongosh):
    #   db.tracks.deleteOne({ _id: "demo_track_001" })
    #
    # SQL:
    #   DELETE FROM tracks WHERE id = 'demo_track_001';
    #   (artists/genres rows in other tables need ON DELETE CASCADE,
    #    in MongoDB they live inside the document, so they go with it)
    result = tracks.delete_one({"_id": TRACK_ID})

    after = tracks.count_documents({})
    print(f"Deleted: {result.deleted_count}")
    print(f"Documents before: {before}, after: {after}")


if __name__ == "__main__":
    main()
