from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

app = FastAPI(title="Omni-Route Backend", version="1.0.0")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FlashcardResponse(BaseModel):
    id: int
    front: str
    back: str

def generate_mock_flashcards():
    return [
        {"id": 1, "front": "What is Omni-Route?", "back": "An offline-first educational orchestrator."},
        {"id": 2, "front": "What is the primary constraint?", "back": "4GB VRAM maximum for local model routing."},
        {"id": 3, "front": "What aesthetic is enforced?", "back": "Strictly monochromatic (Black and White)."},
        {"id": 4, "front": "Which protocol handles local model routing?", "back": "Model Context Protocol (MCP)."},
        {"id": 5, "front": "What happens after 3 failed attempts?", "back": "The Three-Fail Fallback protocol escalates to the user or a safe state."}
    ]

@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    """
    Process a PDF document and return mock flashcards.
    Simulates processing delay.
    """
    await asyncio.sleep(2) # Simulate processing time for loading skeleton
    return {"filename": file.filename, "flashcards": generate_mock_flashcards()}

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    """
    Process an audio file and return mock flashcards.
    Simulates processing delay.
    """
    await asyncio.sleep(2) # Simulate processing time for loading skeleton
    return {"filename": file.filename, "flashcards": generate_mock_flashcards()}
