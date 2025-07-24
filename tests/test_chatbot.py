import pytest
import httpx
from unittest.mock import patch, MagicMock

# Assuming FastAPI app runs on localhost:8000
BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_chat_endpoint_mocked_llm():
    with patch('google.generativeai.GenerativeModel') as mock_generative_model:
        # Configure the mock LLM to return a predictable response
        mock_instance = MagicMock()
        mock_generative_model.return_value = mock_instance
        mock_instance.generate_content.return_value.text = "LLM response about patient data."

        async with httpx.AsyncClient() as client:
            test_patient_id = "patient_24" # Still relies on data being in DB for context retrieval
            query = f"What is the primary diagnosis for {test_patient_id}?"
            response = await client.post(f"{BASE_URL}/chat", params={"query": query})

            assert response.status_code == 200
            assert "response" in response.json()
            assert isinstance(response.json()["response"], str)
            assert response.json()["response"] == "LLM response about patient data."

            # Verify that generate_content was called
            mock_instance.generate_content.assert_called_once()
