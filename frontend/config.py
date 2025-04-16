import textwrap

# API Base URL
API_BASE_URL = "http://localhost:8000/api"

# Embedding model used for retrieval
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L12-v2"

# Generation model
GENERATION_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
# GENERATION_MODEL = "allenai/OLMo-2-1124-7B-Instruct"

EXISTING_COLLECTION = None
EXISTING_QDRANT_PATH = None

# Retrieval Settings
RETRIEVAL_K = 2  # Number of relevant documents to retrieve

# Expand query with synonyms or additional keywords
def expand_query(query: str) -> str:
    """Modify query for better retrieval."""
    return query

# Prompt template for generation
def format_prompt(context: str, question: str) -> str:
    """Format the retrieval context into the final prompt."""
    return textwrap.dedent(f"""
    You are an medical science expert. Summarize the below papers using a few sentences or bullet point in lay language at a 6th grade reading level, while answering the given question:

    {context}

    Question: {question}
    """)
