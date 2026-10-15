"""INDEX: compare the cost of the same query without and with an index."""
from pymongo import MongoClient

from config import COLLECTION_NAME, DB_NAME, MONGO_URI

QUERY = {"genres": "jazz"}
INDEX_NAME = "genres_1"


def explain_cost(tracks, query):
    """Return (documents examined, execution time in ms) for a query."""
    stats = tracks.find(query).explain()["executionStats"]
    return stats["totalDocsExamined"], stats["executionTimeMillis"]


def main():
    tracks = MongoClient(MONGO_URI)[DB_NAME][COLLECTION_NAME]

    # Start without an index
    if INDEX_NAME in tracks.index_information():
        tracks.drop_index(INDEX_NAME)

    # MongoDB (mongosh):
    #   db.tracks.find({ genres: "jazz" }).explain("executionStats")
    # SQL:
    #   EXPLAIN ANALYZE SELECT * FROM track_genres WHERE genre = 'jazz';
    examined, millis = explain_cost(tracks, QUERY)
    print(f"Without index: {examined} documents examined, {millis} ms")

    # MongoDB (mongosh):
    #   db.tracks.createIndex({ genres: 1 })
    # SQL:
    #   CREATE INDEX idx_genre ON track_genres (genre);
    tracks.create_index("genres")

    examined, millis = explain_cost(tracks, QUERY)
    print(f"With index:    {examined} documents examined, {millis} ms")


if __name__ == "__main__":
    main()
