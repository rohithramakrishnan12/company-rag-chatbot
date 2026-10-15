import fitz, chromadb
import config
from gemini import embed

doc = fitz.open(config.PDF_PATH)

chunks, pages = [], []
for page_no, page in enumerate(doc, start=1):
    current = ""
    for para in page.get_text().split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) < 800:
            current += para + "\n"
        else:
            if current:
                chunks.append(current)
                pages.append(page_no)
            current = para + "\n"
    if current:
        chunks.append(current)
        pages.append(page_no)

print("Chunks created:", len(chunks))
print("First chunk preview:\n", chunks[0][:300])

vectors = embed(chunks, "RETRIEVAL_DOCUMENT")

client = chromadb.PersistentClient(path=config.DB_PATH)
try:
    client.delete_collection(config.COLLECTION)
except Exception:
    pass
col = client.create_collection(config.COLLECTION)
col.add(
    ids=[str(i) for i in range(len(chunks))],
    documents=chunks,
    embeddings=vectors,
    metadatas=[{"page": p} for p in pages],
)
print("Stored", len(chunks), "chunks")