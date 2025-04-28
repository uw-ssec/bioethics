from langchain.schema import Document
from core.retriever.retriever import Retriever


def json_to_document(json_data):
    """Convert JSON dict to LangChain Document object."""
    return Document(page_content=json_data["page_content"], metadata=json_data["metadata"])


def perform_retrieval(documents, query, existing_collection, existing_qdrant_path, embedding_model):
    # Early return if no retrieval sources available
    if not documents and not (existing_collection and existing_qdrant_path):
        return {
            "docs": [],
            "status_code": 200,
            "message": "No documents or existing vector store provided for retrieval",
        }

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

    return {"docs": response_data, "status_code": 200}
