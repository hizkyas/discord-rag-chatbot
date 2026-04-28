import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from loguru import logger

class IngestionService:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_documents(self, directory_path: str) -> List:
        """Loads all PDFs from the specified directory."""
        logger.info(f"Loading documents from {directory_path}")
        loader = DirectoryLoader(directory_path, glob="./*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()
        logger.info(f"Loaded {len(docs)} document pages")
        return docs

    def chunk_documents(self, documents: List) -> List:
        """Splits documents into smaller chunks."""
        logger.info("Chunking documents...")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        return chunks

if __name__ == "__main__":
    # Test logic
    ingestor = IngestionService()
    # Assuming documents are in the 'data' folder
    # docs = ingestor.load_documents("./data")
    # chunks = ingestor.chunk_documents(docs)
