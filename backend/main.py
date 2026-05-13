from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import aiohttp
import json
import tempfile
import os
from docling.document_converter import DocumentConverter

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

def truncate_text_for_vram(text: str, max_words: int = 2000) -> str:
    """
    Truncate text to fit within the 4GB VRAM constraint for the model context.
    """
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "... [TRUNCATED]"
    return text

async def generate_flashcards_with_ollama(text: str) -> list[dict]:
    """
    Call Ollama API with the Three-Fail protocol.
    """
    prompt = f"""
<context>
{text}
</context>

You are an expert educational AI. Based on the context provided above, generate exactly 5 flashcards.
You MUST output your response in strict JSON format. Do not include markdown code blocks or any other text.
The JSON must be an array of objects, where each object has three keys: "id" (integer), "front" (string), and "back" (string).
Example:
[
  {{"id": 1, "front": "Question 1", "back": "Answer 1"}},
  ...
]
"""

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma4:e4b",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=60)) as response:
                    if response.status == 200:
                        data = await response.json()
                        response_text = data.get("response", "[]")
                        try:
                            # Attempt to parse the structured output
                            flashcards = json.loads(response_text)
                            if isinstance(flashcards, list) and len(flashcards) > 0:
                                return flashcards
                        except json.JSONDecodeError:
                            print(f"Attempt {attempt + 1}: Failed to parse JSON from Ollama.")
                    else:
                        print(f"Attempt {attempt + 1}: Ollama returned status {response.status}")
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error connecting to Ollama: {e}")

        if attempt < max_attempts - 1:
            await asyncio.sleep(2) # Backoff before retry

    # Three-Fail fallback
    raise HTTPException(status_code=500, detail="Ollama generation failed after 3 attempts.")


@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    """
    Process a PDF document and return generated flashcards.
    Uses Docling to extract text and Ollama for inference.
    """
    temp_file_path = None
    try:
        # Save file to a temporary location for Docling
        fd, temp_file_path = tempfile.mkstemp(suffix=".pdf")
        with os.fdopen(fd, 'wb') as f:
            content = await file.read()
            f.write(content)

        # Extract text using Docling
        converter = DocumentConverter()
        result = converter.convert(temp_file_path)
        extracted_text = result.document.export_to_markdown()

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract any text from the document.")

        # Apply VRAM constraint
        truncated_text = truncate_text_for_vram(extracted_text)

        # Generate flashcards
        flashcards = await generate_flashcards_with_ollama(truncated_text)

        return {"filename": file.filename, "flashcards": flashcards}

    finally:
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    """
    Process an audio file and return mock flashcards.
    Simulates processing delay.
    """
    await asyncio.sleep(2) # Simulate processing time for loading skeleton
    return {"filename": file.filename, "flashcards": generate_mock_flashcards()}
