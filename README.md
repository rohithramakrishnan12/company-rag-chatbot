# Company Document Chatbot (RAG)

A Retrieval-Augmented Generation (RAG) chatbot that answers questions from a company PDF. It answers only from the document, shows the source pages, and says "I don't have that information" when the answer isn't there.

## How it works
1. **Ingest (run once):** PDF text is extracted, split into chunks, converted to embeddings, and stored in ChromaDB.
2. **Ask (every question):** The question is embedded, the top 3 similar chunks are retrieved, and Gemini writes the answer from them.

## Tech stack
Python, Gemini API (LLM and embeddings), ChromaDB, PyMuPDF, Streamlit, python-dotenv

## Project structure
```
├── app.py            # Streamlit chat app
├── ingest.py         # PDF -> chunks -> embeddings -> ChromaDB
├── gemini.py         # Gemini embed() and generate() with retry
├── config.py         # Settings (models, paths, TOP_K)
├── requirements.txt
└── data/company.pdf  # Source document
```

## Run it locally
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file with your Gemini API key (free from Google AI Studio):
```
GEMINI_API_KEY=your_key_here
```
Then:
```
python ingest.py
streamlit run app.py
```

## Limitations
- One chunk per page can miss details that span pages.
- Only the top 3 chunks are sent to the LLM, so questions that need the whole document (counting, summarizing) are weak.

## Future improvements
Overlapping chunks, re-ranking, support for multiple PDFs, and a REST API.
