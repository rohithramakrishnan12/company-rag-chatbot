from google import genai
from google.genai import types
import config
import time

client = genai.Client(api_key=config.GEMINI_API_KEY)

def embed(texts, task):
    # task: "RETRIEVAL_DOCUMENT" for chunks, "RETRIEVAL_QUERY" for questions
    vectors = []
    for i in range(0, len(texts), 50):
        batch = texts[i:i + 50]
        res = client.models.embed_content(
            model=config.EMBED_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(task_type=task),
        )
        vectors += [e.values for e in res.embeddings]
    return vectors

def generate(prompt):
    for attempt in range(5):
        try:
            res = client.models.generate_content(model=config.LLM_MODEL, contents=prompt)
            return res.text
        except Exception as e:
            if "503" in str(e) and attempt < 4:
                time.sleep(3 * (attempt + 1))   # wait 3s, 6s, 9s, 12s
            else:
                return "The AI model is busy right now. Please try again in a minute."