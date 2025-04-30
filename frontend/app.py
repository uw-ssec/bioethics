from __future__ import annotations

from pathlib import Path

import requests
import streamlit as st  # type: ignore[import]
import urllib3
from config import (
    API_BASE_URL,
    EMBEDDING_MODEL,
    EXISTING_COLLECTION,
    EXISTING_QDRANT_PATH,
    GENERATION_MODEL,
    PROMPT_TEMPLATES,
)
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Initialize session state for messages if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Bioethics RAG Chatbot")

# Template selection with "No Template" as the default option
template_options = ["No Template", *list(PROMPT_TEMPLATES.keys())]
selected_template = st.selectbox("Choose a prompt template", template_options, index=0)

# Show text area only if a template is selected
if selected_template != "No Template":
    user_template = st.text_area(
        "Customize template", value=PROMPT_TEMPLATES[selected_template], height=250
    )
else:
    # When "No Template" is selected, no text area is shown
    # But we need to define user_template for later use
    user_template = ""

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("chunks"):
            st.markdown("### Retrieved Document Chunks:")
            for chunk in message["chunks"]:
                st.markdown(f"- {chunk}")

# File uploader for documents
uploaded_files = st.file_uploader(
    "Attach documents (PDFs)", type=["pdf"], accept_multiple_files=True
)


# Function to process uploaded PDFs
def process_uploaded_files(uploaded_files):
    """Reads uploaded PDF files and extracts text + metadata."""
    documents = []
    for file in uploaded_files:
        with Path(file.name).open("wb") as f:
            f.write(file.getbuffer())
        loader = PyMuPDFLoader(file.name)  # Load PDF
        pages = loader.load()

        for page in pages:
            chunks = text_splitter.split_text(page.page_content)
            for i, chunk in enumerate(chunks):
                documents.append({"page_content": chunk, "metadata": {**page.metadata, "chunk": i}})

    return documents


def retrieve_response(query, documents):
    """
    Calls the backend retrieval API to fetch relevant documents based on the query.

    Parameters:
        query (str): The user's question or search query
        documents (list): List of PDF dicts with page_content and metadata

    Returns:
        dict: JSON response from the API containing:
            - docs: List of retrieved document chunks
            - status_code: HTTP status code of the response
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/retrieve/",
            json={
                "query": query,
                "documents": documents,
                "embedding_model": EMBEDDING_MODEL,
                "existing_collection": EXISTING_COLLECTION,
                "existing_qdrant_path": EXISTING_QDRANT_PATH,
            },
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"❌ Retrieval API failed: {e!s}")
        return {"docs": []}


def generate_response(prompt):
    """
    Calls the backend generation API to produce a generated answer to the prompt.

    Parameters:
        prompt (str): a formatted prompt ready to send to the generation model
        generation_model (str): The model to use for text generation

    Returns:
        dict: JSON response from the API containing:
            - answer: The generated text response
            - status_code: HTTP status code of the response
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate/",
            json={"prompt": prompt, "generation_model": GENERATION_MODEL},
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"❌ Generation API failed: {e!s}")
        return {"answer": "⚠️ Failed to generate response."}


# Process PDFs only if uploaded
documents = process_uploaded_files(uploaded_files) if uploaded_files else []

# User input for question
if query := st.chat_input("Your question:"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Retrieving relevant documents..."):
        retrieved_docs = retrieve_response(query, documents).get("docs", [])
        if not retrieved_docs:  # Handle case where no docs returned
            retrieved_docs = []
            retrieved_text = ""
        else:
            retrieved_text = "\n\n".join(doc["page_content"] for doc in retrieved_docs)

    # Show retrieved documents immediately
    if retrieved_docs:
        with st.chat_message("assistant"):
            st.markdown("### Retrieved Document Chunks:")
            for doc in retrieved_docs:
                st.markdown(f"- {doc['page_content'][:500]}")

    # Generate response using retrieved documents as context
    with st.spinner("Generating response..."):
        if selected_template == "No Template":
            # If "No Template" is selected, use just the query
            formatted_prompt = query
        else:
            # Otherwise use the template (either selected or custom)
            formatted_prompt = user_template.format(context=retrieved_text, question=query)
        generate_response_data = generate_response(formatted_prompt)
        if "answer" in generate_response_data:
            generated_answer = generate_response_data["answer"]
        else:
            st.error("⚠️ Unable to generate a response. Please try again later.")
            generated_answer = "⚠️ Failed to generate response."

    # Display AI-generated response
    assistant_message = {
        "role": "assistant",
        "content": generated_answer,
        "chunks": [doc["page_content"][:500] for doc in retrieved_docs],
    }
    st.session_state.messages.append(assistant_message)

    with st.chat_message("assistant"):
        st.markdown(generated_answer)
