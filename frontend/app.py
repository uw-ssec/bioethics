import streamlit as st
import requests
import json
import time
from langchain.document_loaders import PyMuPDFLoader
import urllib3
from io import BytesIO
from docx import Document
from config import (
    API_BASE_URL, 
    EMBEDDING_MODEL, 
    GENERATION_MODEL, 
    RETRIEVAL_K, 
    EXISTING_COLLECTION, 
    EXISTING_QDRANT_PATH, 
    expand_query, 
    format_prompt
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize session state for messages if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

# Predefined templates based on PR #3
TEMPLATES = {
    "Research Summary (Default)": """
    You are a medical science expert. Summarize the below papers using a few sentences or bullet points in lay language at a 6th grade reading level, while answering the given question:

    {context}

    Question: {question}
    """,
    
    "Detailed Research Report": """
    You are a medical science expert and have to write a report on the below papers:
    
    {context}
    
    Write a summary to communicate the research to study participants in a few sentences for each section. Write in lay language at a 6th grade reading level.

    Headings for the summary:
    - What was the research about?
    - How was the research done?
    - What did the researchers learn? (Answer this in detailed bullet points)
    - What was new and innovative about the studies?
    - What do the findings mean?
    - What's next?

    Question: {question}
    """,
    
    "Technical Analysis": """
    As a medical researcher, provide a detailed technical analysis of the following papers, focusing on methodology and results:

    {context}

    Specific aspects to address:
    1. Research methodology
    2. Statistical significance
    3. Key findings
    4. Limitations
    5. Future research directions

    Question: {question}
    """,
    
    "Patient Communication": """
    As a healthcare provider, explain the following research in simple terms that patients can understand:

    {context}

    Please cover:
    - What this means for patients
    - Practical implications
    - What patients should know
    - Next steps

    Question: {question}
    """,
    
    "Policy Brief": """
    Synthesize the following research into a policy brief format:

    {context}

    Structure:
    1. Executive Summary
    2. Key Findings
    3. Policy Implications
    4. Recommendations
    5. Implementation Considerations

    Question: {question}
    """
}

st.title("RAG Chatbot")

# Template selection
selected_template = st.selectbox(
    "Choose a prompt template",
    list(TEMPLATES.keys()),
    index=0
)

# Show and allow editing of the selected template
user_template = st.text_area(
    "Customize template (optional)",
    value=TEMPLATES[selected_template],
    height=250
)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("chunks"):
            st.markdown("### Retrieved Document Chunks:")
            for chunk in message["chunks"]:
                st.markdown(f"- {chunk}")

# File uploader for documents
uploaded_files = st.file_uploader("Attach documents (PDFs)", type=["pdf"], accept_multiple_files=True)

# Function to process uploaded PDFs
def process_uploaded_files(uploaded_files):
    """Reads uploaded PDF files and extracts text + metadata."""
    documents = []
    for file in uploaded_files:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        loader = PyMuPDFLoader(file.name)  # Load PDF
        pages = loader.load()

        for page in pages:
            documents.append({
                "page_content": page.page_content,
                "metadata": page.metadata
            })

    return documents

# Function to call the backend retrieval API
def retrieve_response(query, documents):
    """Call the backend retrieval API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/retrieve/",
            json={"query": query, "documents": documents, "embedding_model": "default_model"},
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"❌ Retrieval API failed: {str(e)}")
        return {"retrieved_docs": []}

# Function to call the backend generation API
def generate_response(prompt):
    """Call the backend generation API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate/",
            json={"prompt": prompt},
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"❌ Generation API failed: {str(e)}")
        return {"answer": "⚠️ Failed to generate response."}

# Process PDFs only if uploaded
documents = process_uploaded_files(uploaded_files) if uploaded_files else []

# User input for question
if query := st.chat_input("Your question:"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Retrieving relevant documents..."):
        retrieved_docs = retrieve_response(query, documents).get("retrieved_docs", [])

    # Show retrieved documents immediately
    retrieved_text = "\n\n".join(doc["page_content"] for doc in retrieved_docs)
    if retrieved_docs:
        with st.chat_message("assistant"):
            st.markdown("### Retrieved Document Chunks:")
            for doc in retrieved_docs:
                st.markdown(f"- {doc['page_content'][:500]}")

    # Generate response using retrieved documents as context
    with st.spinner("Generating response..."):
        formatted_prompt = user_template.format(
            context=retrieved_text,
            question=query
        )
        generate_response_data = generate_response(formatted_prompt)
        generated_answer = generate_response_data.get("answer", "⚠️ Failed to generate response.")

    # Display AI-generated response
    assistant_message = {
        "role": "assistant",
        "content": generated_answer,
        "chunks": [doc["page_content"][:500] for doc in retrieved_docs]
    }
    st.session_state.messages.append(assistant_message)

    with st.chat_message("assistant"):
        st.markdown(generated_answer)
