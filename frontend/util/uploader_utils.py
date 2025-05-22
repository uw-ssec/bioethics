from __future__ import annotations

import re
from pathlib import Path

from config import CHUNK_OVERLAP, CHUNK_SIZE, filter_keywords
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)


def is_noise_chunk(chunk: str) -> bool:
    noise_patterns = [
        r"^\s*©",
        r"copyright",
        r"ceur workshop",
        r"issn",
        r"arxiv",
        r"http[s]?://",
        r"license",
        r"all rights reserved",
    ]
    chunk_lower = chunk.lower()
    return any(re.search(pat, chunk_lower) for pat in noise_patterns)


def process_uploaded_files(uploaded_files):
    """Reads uploaded PDF files and extracts text + metadata."""
    documents = []

    for file in uploaded_files:
        with Path(file.name).open("wb") as f:
            f.write(file.getbuffer())
        loader = PyMuPDFLoader(file.name)
        pages = loader.load()

        for page in pages:
            page_content_lower = page.page_content.lower()
            skip_page = False
            for keyword in filter_keywords:
                if (
                    keyword in page_content_lower
                    and (
                        page.page_content.count(keyword) > 1
                        or any(
                            line.strip().lower().startswith(keyword)
                            for line in page.page_content.split("\n")
                        )
                    )
                    and re.search(
                        r"^\s*(" + keyword + r")\s*$\n",
                        page.page_content,
                        re.IGNORECASE | re.MULTILINE,
                    )
                ):
                    skip_page = True
                    break
            if skip_page:
                continue

            chunks = text_splitter.split_text(page.page_content)
            for i, chunk in enumerate(chunks):
                if is_noise_chunk(chunk):
                    continue
                documents.append({"page_content": chunk, "metadata": {**page.metadata, "chunk": i}})

    return documents
