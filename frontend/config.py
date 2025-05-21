from __future__ import annotations

from docx.shared import RGBColor

# API Base URL
API_BASE_URL = "http://localhost:8000/api"

# Embedding model used for retrieval
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L12-v2"

# Generation model
GENERATION_MODEL = "llama3.2"

EXISTING_COLLECTION = None
EXISTING_QDRANT_PATH = None

# Text processing parameters
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 120

# Docx styling
UW_PURPLE = RGBColor.from_string("4B2E83")

# Keywords to filter out pages/chunks
filter_keywords = [
    "references",
    "acknowledgements",
    "author contributions",
    "bibliography",
    "funding",
]

PROMPT_TEMPLATES = {
    "Research Summary": """
    You are a medical science expert. Summarize the below papers using a few sentences or bullet points in lay language at a 6th grade reading level. Focus on the main findings and significance for a general audience.

    Below is the research content to summarize:
    {context}
    """,
    "Detailed Research Report": """
    You are a medical science expert and have to write a report on the below papers.

    Below is the research content to analyze:
    {context}

    Write a summary to communicate the research to study participants in a few sentences for each section. Write in lay language at a 6th grade reading level.

    Headings for the summary:
    - What was the research about?
    - How was the research done?
    - What did the researchers learn? (Answer this in detailed bullet points)
    - What was new and innovative about the studies?
    - What do the findings mean?
    - What's next?
    """,
    "Technical Analysis": """
    As a medical researcher, provide a detailed technical analysis of the following papers, focusing on methodology and results.

    Below is the research content to analyze:
    {context}

    Specific aspects to address:
    1. Research methodology
    2. Statistical significance
    3. Key findings
    4. Limitations
    5. Future research directions
    """,
    "Patient Communication": """
    As a healthcare provider, explain the following research in simple terms that patients can understand.

    Below is the research content to explain:
    {context}

    Please cover:
    - What this means for patients
    - Practical implications
    - What patients should know
    - Next steps
    """,
    "Policy Brief": """
    Synthesize the following research into a policy brief format.

    Below is the research content to synthesize:
    {context}

    Structure:
    1. Executive Summary
    2. Key Findings
    3. Policy Implications
    4. Recommendations
    5. Implementation Considerations
    """,
}
