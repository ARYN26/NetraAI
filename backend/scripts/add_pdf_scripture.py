"""Script to add PDF books to the knowledge base."""
import sys
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from PyPDF2 import PdfReader
from loguru import logger

from app.services.knowledge_base import KnowledgeBase


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text from all pages
    """
    logger.info(f"Extracting text from: {pdf_path}")

    reader = PdfReader(pdf_path)
    text_parts = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            # Clean up the text
            text = clean_text(text)
            text_parts.append(text)
            logger.debug(f"Page {i+1}: {len(text)} chars")

    full_text = "\n\n".join(text_parts)
    logger.info(f"Extracted {len(full_text)} characters from {len(reader.pages)} pages")

    return full_text


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.

    - Remove excessive whitespace
    - Remove page numbers
    - Fix common OCR issues
    """
    # Remove page numbers (lines that are just numbers)
    text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)

    # Remove excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove excessive spaces
    text = re.sub(r' {2,}', ' ', text)

    # Fix common hyphenation at line breaks
    text = re.sub(r'-\n', '', text)

    # Strip each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()


def add_pdf_to_knowledge_base(pdf_path: str, source_name: str, description: str = "") -> int:
    """
    Extract text from PDF and add to knowledge base.

    Args:
        pdf_path: Path to the PDF file
        source_name: Name for the source (e.g., "A Million Thoughts - Om Swami")
        description: Optional description of the content

    Returns:
        Number of chunks added
    """
    # Extract text
    text = extract_text_from_pdf(pdf_path)

    if not text:
        logger.error("No text extracted from PDF")
        return 0

    # Initialize knowledge base
    kb = KnowledgeBase()

    # Add to knowledge base using source_url parameter
    source_url = f"book://{source_name}"
    chunks_added = kb.add_text(text=text, source_url=source_url)

    logger.success(f"Added {chunks_added} chunks from '{source_name}'")
    return chunks_added


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.add_pdf_scripture <pdf_path> <source_name> [description]")
        print("")
        print("Example:")
        print('  python -m scripts.add_pdf_scripture "/path/to/book.pdf" "A Million Thoughts - Om Swami" "Meditation guide"')
        sys.exit(1)

    pdf_path = sys.argv[1]
    source_name = sys.argv[2]
    description = sys.argv[3] if len(sys.argv) > 3 else ""

    # Validate PDF exists
    if not Path(pdf_path).exists():
        logger.error(f"PDF file not found: {pdf_path}")
        sys.exit(1)

    # Add to knowledge base
    chunks = add_pdf_to_knowledge_base(pdf_path, source_name, description)

    if chunks > 0:
        print(f"\nSuccessfully added '{source_name}' to knowledge base ({chunks} chunks)")
    else:
        print(f"\nFailed to add '{source_name}' to knowledge base")
        sys.exit(1)


if __name__ == "__main__":
    main()
