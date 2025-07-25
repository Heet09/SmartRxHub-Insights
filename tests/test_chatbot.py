import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from api.main import app, get_chatbot # Import app and the dependency

# Assuming FastAPI app runs on localhost:8000
BASE_URL = "http://localhost:8000"

@pytest.fixture
def mock_chatbot():
    mock = MagicMock()
    mock.ask.return_value = "Mocked LLM response about patient data."
    return mock

@pytest.mark.asyncio
async def test_chat_endpoint_mocked_llm(mock_chatbot):
    app.dependency_overrides[get_chatbot] = lambda: mock_chatbot

    with TestClient(app) as client:
        test_patient_id = "patient_24" # Still relies on data being in DB for context retrieval
        query = f"What is the primary diagnosis for {test_patient_id}?"
        response = client.post("/chat", params={"query": query})

        assert response.status_code == 200
        assert "response" in response.json()
        assert isinstance(response.json()["response"], str)
        assert response.json()["response"] == "Mocked LLM response about patient data."

        # Verify that the ask method was called
        mock_chatbot.ask.assert_called_once_with(query)

    # Clean up the dependency override
    app.dependency_overrides = {}
