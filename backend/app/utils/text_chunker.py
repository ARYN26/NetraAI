"""Smart text chunking with overlap for better RAG retrieval."""
import re
from typing import List
from loguru import logger


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> List[str]:
    """
    Split text into overlapping chunks using smart boundaries.

    This implementation tries to split on sentence/paragraph boundaries
    to preserve semantic coherence, rather than splitting mid-sentence.

    Args:
        text: The text to chunk
        chunk_size: Target size for each chunk (characters)
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not text or len(text) < 50:
        return []

    # Clean the text
    text = text.strip()

    # If text is smaller than chunk size, return as single chunk
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        # Calculate end position
        end = start + chunk_size

        # If this isn't the last chunk, try to find a good break point
        if end < len(text):
            # Look for paragraph break first (within last 200 chars)
            search_start = max(start + chunk_size - 200, start)
            para_match = find_last_match(text[search_start:end], r"\n\n")
            if para_match:
                end = search_start + para_match

            # Otherwise, look for sentence end
            elif (sent_match := find_last_match(text[search_start:end], r"[.!?]\s")):
                end = search_start + sent_match + 1  # Include the punctuation

            # Otherwise, look for any whitespace
            elif (space_match := find_last_match(text[search_start:end], r"\s")):
                end = search_start + space_match

        # Extract chunk
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start position (with overlap)
        start = end - overlap if end < len(text) else len(text)

    logger.debug(f"Created {len(chunks)} chunks from {len(text)} characters")
    return chunks


def find_last_match(text: str, pattern: str) -> int | None:
    """
    Find the position of the last match of a pattern.

    Args:
        text: Text to search in
        pattern: Regex pattern to find

    Returns:
        Position of last match, or None if not found
    """
    matches = list(re.finditer(pattern, text))
    if matches:
        return matches[-1].end()
    return None


def chunk_by_sentences(text: str, max_sentences: int = 5) -> List[str]:
    """
    Alternative chunking strategy: split by sentence count.

    Args:
        text: The text to chunk
        max_sentences: Maximum sentences per chunk

    Returns:
        List of text chunks
    """
    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = []

    for sentence in sentences:
        current_chunk.append(sentence)

        if len(current_chunk) >= max_sentences:
            chunks.append(" ".join(current_chunk))
            # Keep last sentence for overlap
            current_chunk = [current_chunk[-1]] if current_chunk else []

    # Add remaining sentences
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
