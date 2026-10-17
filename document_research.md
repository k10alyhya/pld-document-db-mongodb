# Research Summary: Document Data Model (MongoDB)

## 1. What is the Document Model and Why Does It Exist?
The Document Data Model is a non-relational (NoSQL) database paradigm that stores data as semi-structured, self-contained documents (typically JSON or BSON format) rather than strict rows and columns. 

Modern applications require flexible data handling that can scale easily and evolve alongside software development. Traditional relational databases force developer data into rigid schemas, requiring complex migrations when requirements change. The document model bridges this gap by aligning the database structure directly with object-oriented application code, allowing developers to build faster, handle unstructured and semi-structured workloads, and achieve horizontal scalability.

---

## 2. Core Concepts, Data Source & Representation

Unlike relational databases, MongoDB structures its data hierarchically using different terminology:

* **Collection:** Equivalent to a relational `Table`. It is a grouping of related documents.
* **Document:** Equivalent to a relational `Row`. A single record composed of field-value pairs.
* **Field:** Equivalent to a relational `Column`. A key within a document that holds a value.

### Data Source & Preprocessing
For our project, we used the **Spotify Tracks Dataset** from Kaggle, originally provided as a CSV file (`dataset.csv`). Using a custom preprocessing script (`prepare_data.py`), we transformed the tabular data into JSON documents (`tracks.json`):

* **Data Aggregation:** The raw dataset contained **114,000 rows**. Because songs were repeated for every genre they belonged to, we merged duplicate tracks into **89,741 unique track documents**.
* **Embedded Arrays:** Duplicate genre rows were consolidated into a single `genres` array per track (e.g., a "Comedy" track aggregated 4 genres within a single document).
* **Nested Structures:** Individual acoustic attribute columns were grouped into a nested object called `audio_features`.

### Relationship Strategies: Embedding vs. Referencing
1. **Embedding (Nested Documents):** Related data is stored directly inside a single parent document (e.g., embedding artist arrays and `audio_features` directly inside the track document). 
   * *Pros:* Fast read performance; retrieves all track details in a single I/O query without joins.
   * *Cons:* Document size limit (16MB in MongoDB); risk of data duplication across documents.
2. **Referencing:** Documents store references (ObjectIDs) pointing to documents in other collections, similar to foreign keys in SQL.
   * *Pros:* Prevents data duplication; suitable for large or many-to-many relationships.
   * *Cons:* Requires additional queries or `$lookup` operations to join data.

---

## 3. Basic CRUD Operations & POC Implementation

MongoDB operations map cleanly to standard CRUD operations:
* **Create:** `insertOne()` or `insertMany()` to add new documents into a collection.
* **Read:** `find()` or `findOne()` to query documents based on conditions.
* **Update:** `updateOne()` or `updateMany()` using atomic operators like `$set`, `$push`, or `$inc`.
* **Delete:** `deleteOne()` or `deleteMany()` to remove data.

### Features Explored in Proof of Concept (POC)
In our Python POC, we implemented operations tailored to our Spotify dataset:

* **Nested Queries with Dot Notation:** Querying embedded documents inside `audio_features` (e.g., filtering tracks where `audio_features.danceability > 0.9`).
* **Array Operations & Flexible Updates (`update.py`):** Modifying fields using `$set` on standard fields, updating nested fields within `audio_features`, and pushing new genres to the `genres` array using `$push`.
* **Flexible Schema Demonstration (`create.py`):** Inserting a new track document with a distinct structure (e.g., omitting the `genres` array and adding a new `label` field) into the same `tracks` collection, demonstrating the dynamic nature of flexible schemas.

---

## 4. Performance & Indexing Analysis

A critical finding during our exploration was database indexing behavior, tested in `index_demo.py`:

* **Default Behavior:** MongoDB automatically indexes only the `_id` field.
* **Query Execution Plans (COLLSCAN vs. IXSCAN):** Without a custom index, executing a query like `{genres: "jazz"}` results in a **Collection Scan (`COLLSCAN`)**, forcing the database to inspect every document in the collection. Creating an index converts the query to an **Index Scan (`IXSCAN`)**, retrieving matching documents instantly.
* **Multikey Indexes:** Indexing the `genres` array automatically creates a **Multikey Index**, indexing every element within the array.
* **Trade-offs of Indexing:** Indexes improve read query performance significantly but incur costs: they consume extra memory/disk space and slow down write performance (`insert`, `update`, `delete`).
* **Takeaway:** *"Flexibility is a responsibility."* Query optimization and data structuring become the developer's responsibility rather than being strictly enforced by the database engine.

---

## 5. Strengths, Trade-offs, and Database Comparison

### Strengths & Ideal Use Cases
* **Flexible Schema:** Fields can evolve dynamically without modifying entire collections or taking the database offline. (Note: MongoDB can enforce validation rules if strict constraints are required).
* **High Read Performance:** Embedded data structures eliminate network latency caused by multi-table joins.
* **Ideal Scenarios:** Media catalogs (like Spotify tracks), Content Management Systems (CMS), e-commerce product listings, and real-time user activity tracking.

### Trade-offs & Limitations
* **Lack of Enforced Integrity:** Foreign key relationships and cascade rules are not natively enforced at the database level.
* **Data Duplication & Storage Overhead:** Denormalization increases document size. In our project, converting the original 20MB `dataset.csv` into `tracks.json` expanded the file size to **41MB**, primarily due to repeating key names within every document.

### Comprehensive Model Comparison
| Feature | Document Model (MongoDB) | Relational Model (SQL) | Key-Value Model (e.g., Redis) |
| :--- | :--- | :--- | :--- |
| **Data Structure** | Flexible JSON/BSON Documents | Rigid Tables, Rows & Columns | Key-Value Pairs |
| **Query Expressiveness** | High (Rich filtering, aggregations) | Very High (Complex SQL queries) | Low (Primary key lookups) |
| **Relationships** | Embedded or Referenced | Enforced Foreign Keys & JOINs | None (Handled by application) |
| **Best For** | Rapid iteration, media catalogs | Financial records, strict ACID transactions | Caching, session management, speed |

---

## 6. Most Useful Findings & What Surprised Us

* **Most Useful Finding:** Aggregating relational CSV rows into single documents with embedded arrays (`genres`) completely eliminated the need for complex junction tables and SQL `JOIN` statements.
* **What Surprised Us:** The storage trade-off caused by schema flexibility. Seeing the data size grow from **20MB (CSV)** to **41MB (JSON)** due to repeated field names in every document highlighted the real-world storage cost of document denormalization.

---

## 7. Role in Polyglot Persistence Architecture

Modern enterprise applications rarely rely on a single database. In a **Polyglot Persistence** architecture, each database model handles the specific workload it does best:

* **MongoDB Role:** Serves as the primary operational store for flexible catalog data, track metadata, user playlists, and artist profiles.
* **Coexistence with other models:**
  * *Relational Database (e.g., PostgreSQL):* Handles financial transactions, subscription billing, and user payment histories where strict multi-table ACID transactions are required.
  * *Key-Value Store (e.g., Redis):* Caches high-frequency read data (like trending track lists or active user session tokens) to minimize load on MongoDB.

---

## 8. Citations & Resources

1. MongoDB, Inc. *MongoDB Documentation: The Document Data Model*. Available at: [https://www.mongodb.com/docs/manual/core/data-modeling-introduction/](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/)
2. MongoDB, Inc. *Embedded Data Models vs. References*. Available at: [https://www.mongodb.com/docs/manual/core/data-model-design/](https://www.mongodb.com/docs/manual/core/data-model-design/)
3. Martin Fowler. *Polyglot Persistence*. Available at: [https://martinfowler.com/bliki/PolyglotPersistence.html](https://martinfowler.com/bliki/PolyglotPersistence.html)
4. Kaggle. *Spotify Tracks Dataset*. Available at: [https://www.kaggle.com/datasets/maharshipandya/spotify-tracks-dataset](https://www.kaggle.com/datasets/maharshipandya/spotify-tracks-dataset)
