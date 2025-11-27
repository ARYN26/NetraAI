"""
Seed scriptures into ChromaDB knowledge base.

This script loads pre-curated tantric scripture files into the knowledge base
for Netra to use when answering questions.

Usage:
    python -m scripts.seed_scriptures           # Load if empty
    python -m scripts.seed_scriptures --force   # Clear and reload
"""
import os
import sys
from pathlib import Path
from typing import List, Tuple

# Add the backend directory to path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from loguru import logger


# Scripture file metadata
SCRIPTURE_FILES = [
    {
        "filename": "shiva_purana_worship.txt",
        "source": "Shiva Purana - Vidyeśvarasaṃhitā",
        "description": "Mode of worshipping Shiva, daily puja procedures, abhisheka rituals",
    },
    {
        "filename": "shiva_anusthan_vidhi.txt",
        "source": "Traditional Shaiva Anusthan Guidelines",
        "description": "11-day Shiva anusthan procedures, sadhana rules, fasting guidelines",
    },
    {
        "filename": "vijnana_bhairava_112.txt",
        "source": "Vijnana Bhairava Tantra",
        "description": "112 meditation techniques revealed by Lord Shiva",
    },
    {
        "filename": "mantra_japa_guidelines.txt",
        "source": "Traditional Japa Shastra",
        "description": "Mantra japa rules, mala guidelines, purascharana procedures",
    },
]


def get_scripture_dir() -> Path:
    """Get the path to the scriptures directory."""
    return Path(__file__).parent.parent / "data" / "scriptures"


def load_scripture_file(filepath: Path) -> str:
    """Load and return content from a scripture file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return ""


def seed_scriptures(force: bool = False) -> Tuple[int, int]:
    """
    Seed scriptures into the knowledge base.

    Args:
        force: If True, clear existing data and reload

    Returns:
        Tuple of (files_processed, total_chunks_added)
    """
    from app.services.knowledge_base import KnowledgeBase

    kb = KnowledgeBase()
    scripture_dir = get_scripture_dir()

    # Check if already seeded (unless force)
    if not force and kb.collection.count() > 0:
        logger.info(f"Knowledge base already has {kb.collection.count()} chunks. Use --force to reload.")
        return 0, 0

    # Clear if force
    if force:
        logger.info("Clearing existing knowledge base...")
        kb.clear()

    files_processed = 0
    total_chunks = 0

    for scripture in SCRIPTURE_FILES:
        filepath = scripture_dir / scripture["filename"]

        if not filepath.exists():
            logger.warning(f"Scripture file not found: {filepath}")
            continue

        logger.info(f"Loading: {scripture['filename']}")

        content = load_scripture_file(filepath)
        if not content:
            continue

        # Use source as the URL/identifier
        source = f"scripture://{scripture['source']}"

        chunks_added = kb.add_text(content, source)
        total_chunks += chunks_added
        files_processed += 1

        logger.info(f"  Added {chunks_added} chunks from {scripture['description']}")

    logger.success(f"Seeding complete: {files_processed} files, {total_chunks} total chunks")
    return files_processed, total_chunks


def is_knowledge_base_empty() -> bool:
    """Check if the knowledge base is empty."""
    from app.services.knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    return kb.collection.count() == 0


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Seed tantric scriptures into Netra knowledge base"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Clear existing data and reload all scriptures"
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Only check if seeding is needed"
    )

    args = parser.parse_args()

    # Configure logging
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    )

    if args.check:
        empty = is_knowledge_base_empty()
        if empty:
            logger.info("Knowledge base is empty - seeding needed")
            sys.exit(1)
        else:
            from app.services.knowledge_base import KnowledgeBase
            kb = KnowledgeBase()
            logger.info(f"Knowledge base has {kb.collection.count()} chunks")
            sys.exit(0)

    files, chunks = seed_scriptures(force=args.force)

    if files == 0 and not args.force:
        logger.info("No seeding performed. Use --force to reload.")


if __name__ == "__main__":
    main()
