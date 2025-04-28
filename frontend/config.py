# API Base URL
API_BASE_URL = "http://localhost:8000/api"

# Embedding model used for retrieval
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L12-v2"

# Generation model
GENERATION_MODEL = "meta-llama/Llama-3.2-1B-Instruct"
# GENERATION_MODEL = "allenai/OLMo-2-1124-7B-Instruct"

EXISTING_COLLECTION = None
EXISTING_QDRANT_PATH = None

PROMPT_TEMPLATES = {
    "Research Summary": """
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
    """,
}
