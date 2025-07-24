import os
import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Add the project root to the Python path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import SessionLocal, KnowledgeBase

# Configure Gemini API (replace with your actual API key or environment variable)
# It's recommended to load this from an environment variable for security
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

class Chatbot:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.llm = genai.GenerativeModel('models/gemini-1.5-flash-latest')

    def _get_db_session(self):
        return SessionLocal()

    def _retrieve_context(self, query: str, top_k: int = 3):
        query_embedding = self.embedding_model.encode(query).tolist()
        session = self._get_db_session()
        try:
            # Perform similarity search using pgvector's <-> operator
            # Order by distance and limit to top_k results
            results = session.query(KnowledgeBase).order_by(KnowledgeBase.embedding.l2_distance(query_embedding)).limit(top_k).all()
            return [r.content for r in results]
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []
        finally:
            session.close()

    def ask(self, query: str):
        context = self._retrieve_context(query)
        if not context:
            return "I couldn't find relevant information in my knowledge base. Can you please rephrase or provide more details?"

        # Construct the prompt for the LLM
        context_str = "\n".join(context)
        prompt = f"Based on the following information, answer the question:\n\nContext:\n{context_str}\n\nQuestion: {query}\nAnswer:"

        try:
            response = self.llm.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "I'm sorry, I encountered an error while trying to generate a response."

if __name__ == "__main__":
    # Example Usage (for testing the chatbot logic directly)
    chatbot = Chatbot()
    print("Chatbot initialized. Type 'exit' to quit.")
    while True:
        user_query = input("You: ")
        if user_query.lower() == 'exit':
            break
        response = chatbot.ask(user_query)
        print(f"Bot: {response}")
