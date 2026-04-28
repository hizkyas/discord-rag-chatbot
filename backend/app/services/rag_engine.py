import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from backend.app.services.vector_store import VectorStoreService
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class RAGEngine:
    def __init__(self):
        self.vector_store_service = VectorStoreService()
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
        
        self.prompt_template = ChatPromptTemplate.from_template("""
        You are a helpful AI assistant for the Discord RAG Bot project.
        Use the following pieces of retrieved context to answer the user's question accurately.
        If you don't know the answer based on the context, just say that you don't know.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:""")

    def generate_answer(self, query: str):
        """Retrieves context and generates an answer using the LLM."""
        logger.info(f"Generating answer for query: {query}")
        
        # Check for mock mode (if keys are missing)
        if not os.getenv("GOOGLE_API_KEY") or not os.getenv("MONGODB_URI"):
            logger.warning("Running in MOCK MODE due to missing API keys.")
            return {
                "answer": f"This is a MOCK response for: '{query}'. To see real AI answers, please populate your .env file with your API keys.",
                "sources": ["mock_document.pdf"]
            }
        
        # 1. Retrieve context
        docs = self.vector_store_service.similarity_search(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        sources = [doc.metadata.get("source", "Unknown") for doc in docs]
        
        # 2. Generate response
        prompt = self.prompt_template.format(context=context, question=query)
        response = self.llm.invoke(prompt)
        
        return {
            "answer": response.content,
            "sources": list(set(sources))
        }
