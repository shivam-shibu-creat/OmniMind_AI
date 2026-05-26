from fastapi import APIRouter, UploadFile, File

import fitz

from app.utils.chunking import chunk_text

from app.services.embeddings import get_embedding
from app.services.vector_store import add_to_vector_store

router = APIRouter()

@router.post("/upload")
async def upload_files(

    file1: UploadFile = File(...),
    file2: UploadFile = File(None),
    file3: UploadFile = File(None),
    file4: UploadFile = File(None),
    file5: UploadFile = File(None),
    file6: UploadFile = File(None),
    file7: UploadFile = File(None),
    file8: UploadFile = File(None),
    file9: UploadFile = File(None),
    file10: UploadFile = File(None)

):

    files = [
        file1,
        file2,
        file3,
        file4,
        file5,
        file6,
        file7,
        file8,
        file9,
        file10
    ]

    uploaded_files = []

    total_chunks = 0

    for file in files:

        if file is None:
            continue

        pdf_document = fitz.open(
            stream=file.file.read(),
            filetype="pdf"
        )

        file_chunks = 0

        for page_number, page in enumerate(pdf_document):

            text = page.get_text()

            chunks = chunk_text(text)

            file_chunks += len(chunks)

            total_chunks += len(chunks)

            for chunk in chunks:

                embedding = get_embedding(chunk)

                add_to_vector_store(
                    embedding=embedding,
                    chunk=chunk,
                    filename=file.filename,
                    page_number=page_number + 1
                )

        uploaded_files.append({
            "filename": file.filename,
            "chunks": file_chunks
        })

    return {

        "uploaded_files": uploaded_files,

        "total_files": len(uploaded_files),

        "total_chunks": total_chunks,

        "message": "All files stored in vector database"
    }