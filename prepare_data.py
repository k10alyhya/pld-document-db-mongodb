#!/usr/bin/env python3
"""Convert the Spotify tracks CSV into MongoDB-ready JSON documents."""
import csv
import json

INPUT_FILE = "data/dataset.csv"
OUTPUT_FILE = "data/tracks.json"

AUDIO_FEATURES = [
    "danceability", "energy", "key", "loudness", "mode", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
    "time_signature",
]


def build_document(row):
    """Turn one flat CSV row into a nested document."""
    artists = row["artists"].split(";") if row["artists"] else []
    return {
        "_id": row["track_id"],
        "name": row["track_name"],
        "album": row["album_name"],
        "artists": artists,
        "genres": [row["track_genre"]],
        "popularity": int(row["popularity"]),
        "duration_ms": int(row["duration_ms"]),
        "explicit": row["explicit"] == "True",
        "audio_features": {
            feature: float(row[feature]) for feature in AUDIO_FEATURES
        },
    }


def main():
    """Read the CSV, merge duplicate tracks, and write JSON."""
    tracks = {}
    with open(INPUT_FILE, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            track_id = row["track_id"]
            if track_id in tracks:
                genre = row["track_genre"]
                if genre not in tracks[track_id]["genres"]:
                    tracks[track_id]["genres"].append(genre)
            else:
                tracks[track_id] = build_document(row)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(tracks.values()), f, ensure_ascii=False)

    print("Unique tracks written:", len(tracks))


if __name__ == "__main__":
    main()
