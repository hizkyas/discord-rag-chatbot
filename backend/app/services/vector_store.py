import os
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class VectorStoreService:
    def __init__(self):
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("DATABASE_NAME", "discord_rag_bot")
        self.collection_name = os.getenv("COLLECTION_NAME", "knowledge_base")
        self.index_name = os.getenv("VECTOR_INDEX_NAME", "vector_index")
        
        if not self.mongodb_uri:
            logger.warning("MONGODB_URI not found in environment variables.")
            
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.client = MongoClient(self.mongodb_uri)
        self.collection = self.client[self.db_name][self.collection_name]

    def get_vector_store(self):
        """Returns the configured MongoDB Atlas Vector Search instance."""
        return MongoDBAtlasVectorSearch(
            collection=self.collection,
            embedding=self.embeddings,
            index_name=self.index_name
        )

    def add_documents(self, documents):
        """Adds documents to the vector store."""
        logger.info(f"Adding {len(documents)} documents to MongoDB Atlas...")
        vector_store = self.get_vector_store()
        vector_store.add_documents(documents)
        logger.info("Documents successfully added.")

    def similarity_search(self, query: str, k: int = 5):
        """Performs a similarity search for a given query."""
        logger.info(f"Searching for: {query}")
        vector_store = self.get_vector_store()
        results = vector_store.similarity_search(query, k=k)
        return results
