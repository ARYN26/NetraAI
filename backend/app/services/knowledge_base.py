"""Knowledge Base - ChromaDB wrapper for scripture storage and retrieval."""
from typing import List, Tuple, Dict, Any
from loguru import logger

from app.config import settings
from app.utils.text_chunker import chunk_text


class KnowledgeBase:
    """
    Knowledge Base manages scripture text storage and semantic search.

    Uses ChromaDB for:
    - Vector embeddings storage
    - Semantic similarity search
    - Metadata tracking (source URLs)
    """

    def __init__(self):
        """Initialize ChromaDB with persistent storage."""
        try:
            import chromadb
            from chromadb.utils import embedding_functions

            # Create persistent client
            self.client = chromadb.PersistentClient(path=settings.chroma_db_path)

            # Use sentence-transformers for embeddings
            self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=settings.embedding_model
            )

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=settings.chroma_collection_name,
                embedding_function=self.embed_fn,
            )

            logger.info(
                f"KnowledgeBase initialized: {self.collection.count()} chunks in '{settings.chroma_collection_name}'"
            )

        except ImportError:
            raise ImportError(
                "chromadb or sentence-transformers not installed. "
                "Run: pip install chromadb sentence-transformers"
            )

    def add_text(self, text: str, source_url: str) -> int:
        """
        Add text to the knowledge base.

        Args:
            text: The text content to add
            source_url: URL source of the text

        Returns:
            Number of chunks added
        """
        # Chunk the text with smart splitting
        chunks = chunk_text(
            text,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
        )

        if not chunks:
            logger.warning(f"No chunks generated from {source_url}")
            return 0

        # Generate unique IDs
        ids = [f"{source_url}_{i}" for i in range(len(chunks))]

        # Create metadata for each chunk
        metadatas = [{"source": source_url, "chunk_index": i} for i in range(len(chunks))]

        # Upsert (add or update) chunks
        self.collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas,
        )

        logger.info(f"Added {len(chunks)} chunks from {source_url}")
        return len(chunks)

    def search(self, query: str, n_results: int = None) -> Tuple[str, List[str], float]:
        """
        Search for relevant scripture passages.

        Args:
            query: The search query
            n_results: Number of results to return (default from settings)

        Returns:
            Tuple of (combined context string, list of source URLs, best distance score)
            Distance score: lower is better (0 = exact match, 1+ = less relevant)
        """
        if n_results is None:
            n_results = settings.search_results

        # Check if collection has any documents
        if self.collection.count() == 0:
            logger.debug("Knowledge base is empty")
            return "", [], 1.0

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"],  # Include distance scores
            )

            # Extract documents, sources, and distances
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]

            if not documents:
                return "", [], 1.0

            # Get best (lowest) distance score
            best_distance = min(distances) if distances else 1.0

            # Combine documents into context
            context = "\n\n---\n\n".join(documents)

            # Extract unique sources
            sources = list(set(m.get("source", "") for m in metadatas if m.get("source")))

            logger.debug(f"Found {len(documents)} chunks from {len(sources)} sources (best distance: {best_distance:.3f})")
            return context, sources, best_distance

        except Exception as e:
            logger.error(f"Search error: {e}")
            return "", [], 1.0

    def get_stats(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics.

        Returns:
            Dictionary with stats
        """
        count = self.collection.count()

        # Get unique sources
        sources = set()
        if count > 0:
            try:
                # Get all metadatas (limited for performance)
                results = self.collection.get(limit=1000, include=["metadatas"])
                for meta in results.get("metadatas", []):
                    if meta and meta.get("source"):
                        sources.add(meta["source"])
            except Exception as e:
                logger.warning(f"Could not fetch sources: {e}")

        return {
            "total_chunks": count,
            "total_sources": len(sources),
            "collection_name": settings.chroma_collection_name,
        }

    def clear(self) -> None:
        """Clear all data from the knowledge base."""
        # Delete and recreate collection
        self.client.delete_collection(settings.chroma_collection_name)
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            embedding_function=self.embed_fn,
        )
        logger.info("Knowledge base cleared")

    def is_empty(self) -> bool:
        """Check if the knowledge base is empty."""
        return self.collection.count() == 0
