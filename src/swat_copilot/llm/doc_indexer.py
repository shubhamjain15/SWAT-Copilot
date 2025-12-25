"""Document indexing for SWAT documentation."""

import logging
from pathlib import Path
from typing import Optional

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

logger = logging.getLogger(__name__)


class SWATDocumentationIndex:
    """Index and search SWAT documentation."""

    def __init__(
        self,
        docs_path: Path,
        index_path: Optional[Path] = None,
    ) -> None:
        """
        Initialize documentation index.

        Args:
            docs_path: Path to documentation folder
            index_path: Path to store the vector index
        """
        if not LANGCHAIN_AVAILABLE:
            raise ImportError(
                "langchain and dependencies required. "
                "Install with: pip install langchain langchain-community chromadb pypdf sentence-transformers"
            )

        self.docs_path = docs_path
        self.index_path = index_path or docs_path / "vector_index"
        self.vectorstore: Optional[Chroma] = None
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def build_index(self) -> None:
        """Build vector index from documentation."""
        logger.info(f"Building index from {self.docs_path}")

        # Load PDF documents
        pdf_path = self.docs_path / "pdfs"
        documents = []

        if pdf_path.exists():
            logger.info(f"Loading PDFs from {pdf_path}")
            pdf_loader = DirectoryLoader(
                str(pdf_path),
                glob="**/*.pdf",
                loader_cls=PyPDFLoader,
                show_progress=True,
            )
            documents.extend(pdf_loader.load())
            logger.info(f"Loaded {len(documents)} PDF pages")

        # Load text documents
        text_path = self.docs_path / "text"
        if text_path.exists():
            logger.info(f"Loading text files from {text_path}")
            text_loader = DirectoryLoader(
                str(text_path),
                glob="**/*.txt",
                show_progress=True,
            )
            text_docs = text_loader.load()
            documents.extend(text_docs)
            logger.info(f"Loaded {len(text_docs)} text files")

        if not documents:
            logger.warning("No documents found to index")
            return

        logger.info(f"Total documents loaded: {len(documents)}")

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        splits = text_splitter.split_documents(documents)
        logger.info(f"Created {len(splits)} text chunks")

        # Create vector store
        logger.info("Creating vector embeddings (this may take a few minutes)...")
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=str(self.index_path),
        )

        logger.info(f"Index saved to {self.index_path}")

    def load_index(self) -> bool:
        """
        Load existing index.

        Returns:
            True if index loaded successfully
        """
        if not self.index_path.exists():
            logger.warning(f"Index not found at {self.index_path}")
            return False

        try:
            self.vectorstore = Chroma(
                persist_directory=str(self.index_path),
                embedding_function=self.embeddings,
            )
            logger.info("Index loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            return False

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict[str, str]]:
        """
        Search documentation.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of relevant document chunks
        """
        if not self.vectorstore:
            if not self.load_index():
                return []

        results = self.vectorstore.similarity_search(query, k=top_k)

        return [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "page": str(doc.metadata.get("page", "")),
            }
            for doc in results
        ]
