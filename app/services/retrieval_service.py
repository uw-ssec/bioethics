from __future__ import annotations

from typing import Any

from langchain.schema import Document
from typing_extensions import TypedDict

from core.retriever.retriever import Retriever


class DocumentDict(TypedDict):
    page_content: str
    metadata: dict[str, Any]


class RetrievalResult(TypedDict):
    results: list[dict[str, Any]]
    status: str


def json_to_document(json_data: DocumentDict) -> Document:
    """Convert JSON dict to LangChain Document object."""
    return Document(page_content=json_data["page_content"], metadata=json_data["metadata"])


def perform_retrieval(
    documents: list[DocumentDict] | None,
    query: str,
    existing_collection: str | None,
    existing_qdrant_path: str | None,
    embedding_model: str,
) -> RetrievalResult:
    # Early return if no retrieval sources available
    if not documents and not (existing_collection and existing_qdrant_path):
        return {"results": [], "status": "success"}

    # Instantiate the retriever with the provided embedding model
    retriever = Retriever(model_name=embedding_model)

    # Set up the vector store
    if documents:
        # Convert JSON documents to LangChain Document objects
        docs = [json_to_document(doc) for doc in documents]
        retriever.create_vector_store(docs, collection_name="temp_collection")
    else:
        # Use existing vector store
        retriever.get_vector_store(
            qdrant_path=existing_qdrant_path, collection_name=existing_collection
        )

    # Retrieve and format documents
    relevant_docs = retriever.retrieve_docs(query)
    response_data = [
        {"metadata": doc.metadata, "page_content": doc.page_content} for doc in relevant_docs
    ]

    return {"results": response_data, "status": "success"}
