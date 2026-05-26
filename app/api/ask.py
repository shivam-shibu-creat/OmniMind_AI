from fastapi import APIRouter

from pydantic import BaseModel

from app.services.embeddings import get_embedding

from app.services.vector_store import search_vector

from app.services.generator import generate_answer

router = APIRouter()

class AskRequest(BaseModel):

    question: str

class AskResponse(BaseModel):

    question: str

    searched_files: list

    answer: str

    sources: list

@router.post(

    "/ask",

    response_model=AskResponse
)

def ask_question(request: AskRequest):

    question = request.question

    # EMBEDDING

    query_embedding = get_embedding(question)

    # SEARCH

    results = search_vector(

        query_embedding,

        question
    )

    # SORT BY BEST RERANK SCORE

    results = sorted(

        results,

        key=lambda x: x.get(
            "rerank_score",
            0
        ),

        reverse=True
    )

    # CONTEXT

    context = "\n\n".join([

        result["chunk"]

        for result in results
    ])

    # GENERATE ANSWER

    answer = generate_answer(

        question,

        context
    )

    # SEARCHED FILES

    searched_files = []

    seen_files = set()

    for result in results:

        filename = result["filename"]

        if filename not in seen_files:

            seen_files.add(filename)

            searched_files.append(filename)

    # SMART RELEVANT SOURCES

    sources = []

    seen_sources = set()

    answer_lower = answer.lower()

    answer_words = set(

        answer_lower.split()
    )

    for result in results:

        chunk = result["chunk"].lower()

        overlap_count = 0

        for word in answer_words:

            if word in chunk:

                overlap_count += 1

        # ONLY STRONGLY MATCHING CHUNKS

        if overlap_count >= 3:

            source = (

                f"{result['filename']} - "
                f"Page {result['page_number']}"
            )

            if source not in seen_sources:

                seen_sources.add(source)

                sources.append(source)

    # LIMIT SOURCES

    sources = sources[:3]

    return {

        "question": question,

        "searched_files": searched_files[:3],

        "answer": answer,

        "sources": sources
    }