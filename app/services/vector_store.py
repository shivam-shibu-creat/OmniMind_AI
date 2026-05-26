import chromadb

from rank_bm25 import BM25Okapi

from sentence_transformers import CrossEncoder

client = chromadb.PersistentClient(
    path="chromadb_data"
)

collection = client.get_or_create_collection(
    name="documents"
)

# LOAD EXISTING CHUNKS FROM CHROMADB

existing_data = collection.get(

    include=[
        "documents",
        "metadatas"
    ]
)

all_chunks = []

documents = existing_data.get("documents", [])

metadatas = existing_data.get("metadatas", [])

for document, metadata in zip(
    documents,
    metadatas
):

    all_chunks.append({

        "chunk": document,

        "filename": metadata["filename"],

        "page_number": metadata["page_number"]
    })

# CROSS-ENCODER RERANKER

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def add_to_vector_store(
    embedding,
    chunk,
    filename,
    page_number
):

    collection.add(
        embeddings=[embedding],
        documents=[chunk],
        metadatas=[
            {
                "filename": filename,
                "page_number": page_number
            }
        ],
        ids=[
            f"{filename}_{page_number}_{hash(chunk)}"
        ]
    )

    all_chunks.append({

        "chunk": chunk,

        "filename": filename,

        "page_number": page_number
    })

def search_vector(
    query_embedding,
    question,
    filename=None
):

    vector_results = collection.query(

        query_embeddings=[query_embedding],

        n_results=20,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved_chunks = []

    seen_chunks = set()

    # VECTOR SEARCH

    documents = vector_results["documents"][0]

    metadatas = vector_results["metadatas"][0]

    for document, metadata in zip(

        documents,
        metadatas
    ):

        if document in seen_chunks:
            continue

        seen_chunks.add(document)

        retrieved_chunks.append({

            "chunk": document,

            "page_number": metadata["page_number"],

            "filename": metadata["filename"]
        })

    # BM25 SEARCH

    if len(all_chunks) > 0:

        tokenized_chunks = [

            chunk["chunk"].split()

            for chunk in all_chunks
        ]

        bm25 = BM25Okapi(tokenized_chunks)

        tokenized_query = question.split()

        bm25_scores = bm25.get_scores(
            tokenized_query
        )

        top_indices = sorted(

            range(len(bm25_scores)),

            key=lambda i: bm25_scores[i],

            reverse=True

        )[:10]

        for idx in top_indices:

            bm25_chunk = all_chunks[idx]

            if bm25_chunk["chunk"] in seen_chunks:
                continue

            seen_chunks.add(
                bm25_chunk["chunk"]
            )

            retrieved_chunks.append({

                "chunk": bm25_chunk["chunk"],

                "page_number": bm25_chunk["page_number"],

                "filename": bm25_chunk["filename"]
            })

    # FILE FILTER

    if filename:

        retrieved_chunks = [

            result

            for result in retrieved_chunks

            if result["filename"] == filename
        ]

    # RERANKING

    pairs = [

        (question, result["chunk"])

        for result in retrieved_chunks
    ]

    scores = reranker.predict(pairs)

    reranked_results = []

    for result, score in zip(

        retrieved_chunks,
        scores
    ):

        result["rerank_score"] = float(score)

        reranked_results.append(result)

    reranked_results = sorted(

        reranked_results,

        key=lambda x: x["rerank_score"],

        reverse=True
    )

    return reranked_results[:15]