from tools.chunker import chunk_text
from tools.qdrant_store import (
    store_chunks,
    retrieve_chunks
)


def process_document(
    pdf_text,
    query
):

    chunks = chunk_text(pdf_text)

    store_chunks(chunks)

    return {
        "market_chunks":
        retrieve_chunks(
            f"{query} market size competitors funding"
        ),

        "technology_chunks":
        retrieve_chunks(
            f"{query} technology architecture AI models"
        ),

        "trends_chunks":
        retrieve_chunks(
            f"{query} future trends predictions"
        )
    }