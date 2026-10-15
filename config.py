import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = "gemini-3.5-flash-lite"
EMBED_MODEL = "gemini-embedding-001"
PDF_PATH = "data/company.pdf"
DB_PATH = "chroma_db"
COLLECTION = "company"
TOP_K = 3