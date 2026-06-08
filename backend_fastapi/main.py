import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
import tempfile

app = FastAPI(title="Nexus AI Engine")

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_CONNECTION = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/nexus_db")

# Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

class QueryRequest(BaseModel):
    query: str
    course_id: str

@app.post("/api/ai/ingest/")
async def ingest_document(course_id: str, file: UploadFile = File(...)):
    """
    Chunks a PDF, creates embeddings, and stores them in PGVector.
    """
    try:
        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Load and split
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        # Store in PGVector
        vector_db = PGVector.from_documents(
            embedding=embeddings,
            documents=docs,
            collection_name=f"course_{course_id}",
            connection_string=DB_CONNECTION,
        )
        
        os.remove(tmp_path)
        return {"status": "success", "chunks_indexed": len(docs)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from collections import Counter
import re

# ... (Previous imports)

class ConceptGapRequest(BaseModel):
    course_id: str

@app.post("/api/ai/chat/")
async def chat_rag(request: QueryRequest):
    """
    RAG chat filtered by course materials.
    """
    try:
        # Filtering is handled by the collection_name being tied to course_id
        vector_db = PGVector(
            collection_name=f"course_{request.course_id}",
            connection_string=DB_CONNECTION,
            embedding_function=embeddings,
        )
        
        # Using a custom prompt to be more 'Study Buddy' like
        prompt_template = """You are a helpful Study Buddy for this course. 
        Use the following course context to answer the student's question.
        If you don't know the answer based on the context, say you don't know, 
        and suggest they ask the teacher.
        
        Context: {context}
        Question: {question}
        
        Helpful Answer:"""
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_db.as_retriever(search_kwargs={"k": 4}),
        )
        
        response = qa_chain.run(request.query)
        return {"answer": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ai/analytics/concept-gaps/{course_id}")
async def get_concept_gaps(course_id: str):
    """
    Teacher Analytics: Summarizes common keywords from queries (Mock logic for brevity).
    In production, this would query the ChatLog table.
    """
    # Dummy data representing common query topics
    mock_queries = [
        "What is backpropagation?", "How does backpropagation work?",
        "Explain backpropagation again", "What is gradient descent?",
        "Is backpropagation used in CNNs?", "Why is normalization important?"
    ]
    
    # Simple keyword extraction
    all_text = " ".join(mock_queries).lower()
    words = re.findall(r'\w+', all_text)
    # Stop words (simplified)
    stop_words = {'what', 'is', 'how', 'does', 'work', 'again', 'the', 'a', 'in', 'is', 'why'}
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    
    counts = Counter(keywords)
    top_concepts = [{"concept": k, "frequency": v} for k, v in counts.most_common(5)]
    
    return {
        "course_id": course_id,
        "top_gaps": top_concepts,
        "insight": f"Many students are asking about '{top_concepts[0]['concept']}'. Consider a review session."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
