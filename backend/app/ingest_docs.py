import os
from backend.app.services.ingestion import IngestionService
from backend.app.services.vector_store import VectorStoreService
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

def run_ingestion():
    # 1. Check for keys
    if not os.getenv("GOOGLE_API_KEY") or not os.getenv("MONGODB_URI"):
        logger.error("❌ Cannot ingest documents: Missing GOOGLE_API_KEY or MONGODB_URI in .env file.")
        print("\nACTION REQUIRED: Please add your API keys to the .env file before running ingestion.\n")
        return

    logger.info("🚀 Starting ingestion process...")
    
    ingestor = IngestionService()
    vector_store = VectorStoreService()
    
    # 2. Load documents from the 'data' folder (or root if needed)
    # We'll check both the root and the data folder for the project PDF
    data_dir = "./data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    logger.info(f"Scanning {data_dir} for documents...")
    docs = ingestor.load_documents(data_dir)
    
    if not docs:
        logger.warning(f"No documents found in {data_dir}. Checking project root...")
        docs = ingestor.load_documents(".") # Scan root for the project PDF
        
    if not docs:
        logger.error("No PDF documents found to ingest!")
        return

    # 3. Chunk documents
    chunks = ingestor.chunk_documents(docs)
    
    # 4. Add to vector store
    try:
        vector_store.add_documents(chunks)
        logger.info("✅ Ingestion complete! Your knowledge base is now searchable.")
    except Exception as e:
        logger.error(f"❌ Error during vector store upload: {str(e)}")

if __name__ == "__main__":
    run_ingestion()
