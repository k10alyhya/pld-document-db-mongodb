# PLD: Document Database with MongoDB

Proof of concept for the Peer Learning Day on non-relational databases.
The team explored the **document model** using **MongoDB** and a Spotify tracks dataset from Kaggle.

## About the project

The original dataset is a CSV file with about **114,000 rows**. The same track appears
once for every genre it belongs to, so we reshaped it into JSON documents:

- 114,000 CSV rows become **89,741 unique tracks**.
- The repeated genre rows are merged into a single `genres` **array**.
- The audio columns (danceability, energy, tempo, ...) are grouped into a nested
  `audio_features` object.
- The Spotify track id becomes the document `_id`.

Each track is then a single self-contained document. Artists, genres and audio features
live inside the document, so no joins are needed.

## Requirements

- Docker
- Python 3
- `pymongo`

## How to run

Run the steps in this order, from the project folder.

1. Start MongoDB (if the container already exists, use `docker start mongo`):

   ```bash
   docker run --name mongo -p 27017:27017 -d mongo:latest
   ```

2. Install the driver. On recent Ubuntu-based systems pip may refuse to install
   system-wide, so use a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install pymongo
   ```

3. Build `tracks.json` from `dataset.csv`:

   ```bash
   python3 prepare_data.py
   ```

4. Load the data into the `pld_db.tracks` collection (safe to re-run, it recreates the collection):

   ```bash
   python3 import_data.py
   ```

5. Run the CRUD operations in order:

   ```bash
   python3 create.py
   python3 read.py
   python3 update.py
   python3 delete.py
   ```

   `create.py` inserts a fixed `_id`, so running it twice without `delete.py` in between
   reports that the document already exists. That is expected.

6. Compare a query before and after adding an index:

   ```bash
   python3 index_demo.py
   ```

## Files

| File | What it does |
|---|---|
| `config.py` | Shared connection settings (URI, database, collection, data file). Can be overridden with environment variables. |
| `prepare_data.py` | Converts `dataset.csv` into `tracks.json`: merges duplicate rows, builds the `genres` array and the nested `audio_features`. |
| `import_data.py` | Loads `tracks.json` into MongoDB in batches of 5000 documents. |
| `create.py` | **Create**: inserts one document with `insert_one`. Its shape differs from the other tracks (no `genres`, extra `label` field), which shows the flexible schema. |
| `read.py` | **Read**: queries by `_id`, by an array element (`artists`) and by a nested field (`audio_features.danceability`). |
| `update.py` | **Update**: changes a field and a nested field with `$set`, and appends to an array with `$push`. |
| `delete.py` | **Delete**: removes one document with `delete_one` and checks the rest are untouched. |
| `index_demo.py` | **Index**: runs the same query with `explain()` before and after creating an index on `genres`. |

Every script also contains the equivalent mongosh command and SQL statement as comments.

## Document structure

```json
{
  "_id": "5SuOikwiRyPMVoIQDJUgSV",
  "name": "Comedy",
  "album": "Comedy",
  "artists": ["Gen Hoshino"],
  "genres": ["acoustic", "j-pop", "singer-songwriter", "songwriter"],
  "popularity": 73,
  "duration_ms": 230666,
  "explicit": false,
  "audio_features": {
    "danceability": 0.676,
    "energy": 0.461,
    "key": 1.0,
    "loudness": -6.746,
    "mode": 0.0,
    "speechiness": 0.143,
    "acousticness": 0.0322,
    "instrumentalness": 1.01e-06,
    "liveness": 0.358,
    "valence": 0.715,
    "tempo": 87.917,
    "time_signature": 4.0
  }
}
```

- `artists` and `genres` are **arrays**: one track can have several of each.
- `audio_features` is a **nested document**, queried with dot notation (`audio_features.danceability`).

## Index demo

`index_demo.py` runs `find({"genres": "jazz"})` twice and prints how many documents
MongoDB examined and how long it took:

- **Without an index**, MongoDB scans the whole collection.
- **With an index** on `genres`, it only looks at the tracks that match.

Because `genres` is an array, MongoDB builds a multikey index: every element of the
array gets its own entry.

Indexes are not free: they use extra storage and make every insert, update and delete
slightly slower, so only fields that are queried often should be indexed.

## Dataset

Spotify tracks dataset from Kaggle.
