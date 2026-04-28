from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loguru import logger
import os
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from backend.app.services.rag_engine import RAGEngine

load_dotenv()

app = FastAPI(title="Discord RAG Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = RAGEngine()

class QueryRequest(BaseModel):
    user_id: str
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.get("/")
async def root():
    return {"message": "Discord RAG Bot API is running"}

@app.post("/api/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    logger.info(f"Received query from {request.user_id}: {request.query}")
    try:
        result = rag_engine.generate_answer(request.query)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
