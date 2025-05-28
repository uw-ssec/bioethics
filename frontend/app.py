from __future__ import annotations

from pathlib import Path
from typing import Any

import requests  # type: ignore[import-untyped]
import streamlit as st
from config import (
    API_BASE_URL,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    EXISTING_COLLECTION,
    EXISTING_QDRANT_PATH,
    GENERATION_MODEL,
    PROMPT_TEMPLATES,
)
from util.docx_utils import save_to_docx
from util.uploader_utils import process_uploaded_files


def retrieve_response(query: str, documents: list[dict[str, Any]]) -> dict[str, Any]:
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
        return response.json()  # type: ignore[no-any-return]
    except requests.RequestException as e:
        st.error(f"❌ Retrieval API failed: {e!s}")
        return {"docs": []}


def generate_response(prompt: str) -> dict[str, Any]:
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
        return response.json()  # type: ignore[no-any-return]
    except requests.RequestException as e:
        st.error(f"❌ Generation API failed: {e!s}")
        return {"answer": "⚠️ Failed to generate response."}


def handle_submit_button(
    query: str, documents: list[dict[str, Any]], selected_template: str
) -> None:
    retrieved_docs = []
    retrieved_text = ""

    if documents or EXISTING_COLLECTION or EXISTING_QDRANT_PATH:
        with st.spinner("Retrieving relevant documents..."):
            retrieved_docs = retrieve_response(query, documents).get("docs", [])
            retrieved_text = "\n\n".join(
                doc["page_content"] for doc in retrieved_docs if doc.get("page_content")
            )
        if retrieved_docs:
            with st.chat_message("assistant"):
                st.markdown("### Retrieved Document Chunks:")
                for doc in retrieved_docs:
                    st.markdown(f"- {doc['page_content'][:CHUNK_SIZE]}")

    with st.spinner("Generating response..."):
        formatted_prompt = PROMPT_TEMPLATES[selected_template].format(
            query=query, context=retrieved_text
        )
        generate_response_data = generate_response(formatted_prompt)

        if "answer" in generate_response_data:
            generated_answer = generate_response_data["answer"]
            save_to_docx(generated_answer, filename="generated_output.docx")
            with Path("generated_output.docx").open("rb") as f:
                docx_bytes = f.read()
            st.download_button(
                label="Download .docx",
                data=docx_bytes,
                file_name="generated_output.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        else:
            st.error("⚠️ Unable to generate a response. Please try again later.")
            generated_answer = "⚠️ Failed to generate response."

    assistant_message = {
        "role": "assistant",
        "content": generated_answer,
    }
    st.session_state.messages.append(assistant_message)
    with st.chat_message("assistant"):
        st.markdown(generated_answer)


###
# START OF THE STREAMLIT LAYOUT
###
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Bioethics RAG Chatbot")

selected_template = st.selectbox(
    "Choose a prompt template", [*list(PROMPT_TEMPLATES.keys())], index=0
)

# Users can only customize the template if they select templates other than "No Template"
if selected_template != "No Template":
    user_template = st.text_area(
        "Customize template", value=PROMPT_TEMPLATES[selected_template], height=250
    )

uploaded_files = st.file_uploader(
    "Attach documents (PDFs)", type=["pdf"], accept_multiple_files=True
)
documents = process_uploaded_files(uploaded_files) if uploaded_files else []

if selected_template == "No Template":
    # if "No Template" is selected, provide a chat input for the user to ask a question
    if query := st.chat_input("Your question:"):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        handle_submit_button(query, documents, selected_template)
# Otherwise, provide a button to generate a summary/report
elif st.button("Generate Summary/Report"):
    handle_submit_button("", documents, selected_template)
###
# END OF THE STREAMLIT LAYOUT
###
