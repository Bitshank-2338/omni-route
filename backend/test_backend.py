import pytest
from fastapi.testclient import TestClient
from main import app, generate_flashcards_with_ollama
from unittest.mock import patch, AsyncMock
from docling.exceptions import ConversionError

client = TestClient(app)

def test_process_document_success():
    # We must mock Docling to avoid the PDF validity crash during tests
    mock_flashcards = [
        {"id": 1, "front": "Test Front 1", "back": "Test Back 1"},
        {"id": 2, "front": "Test Front 2", "back": "Test Back 2"}
    ]

    with patch("main.DocumentConverter") as mock_converter:
        mock_instance = mock_converter.return_value
        mock_result = mock_instance.convert.return_value
        mock_result.document.export_to_markdown.return_value = "Mocked PDF extracted text"

        with patch("main.generate_flashcards_with_ollama", new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_flashcards

            # Create a dummy PDF file content
            dummy_pdf_content = b"%PDF-1.4 dummy pdf content"

            response = client.post(
                "/process-document",
                files={"file": ("test.pdf", dummy_pdf_content, "application/pdf")}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["filename"] == "test.pdf"
            assert len(data["flashcards"]) == 2
            assert data["flashcards"][0]["front"] == "Test Front 1"

@pytest.mark.asyncio
async def test_three_fail_protocol():
    with patch("aiohttp.ClientSession.post") as mock_post:
        # Mocking the context manager for response
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_post.return_value.__aenter__.return_value = mock_response

        try:
            # We must shorten the sleep during testing to avoid waiting 6 seconds
            with patch("asyncio.sleep", new_callable=AsyncMock):
                await generate_flashcards_with_ollama("Test context")
        except Exception as e:
            assert type(e).__name__ == "HTTPException"
            assert e.status_code == 500
            assert "Ollama generation failed after 3 attempts" in e.detail

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_three_fail_protocol())
    test_process_document_success()
    print("All tests passed!")