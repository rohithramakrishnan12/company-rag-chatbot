import streamlit as st, chromadb
import config
from gemini import embed, generate

st.title("Company Chatbot")

@st.cache_resource
def get_collection():
    return chromadb.PersistentClient(path=config.DB_PATH).get_collection(config.COLLECTION)

col = get_collection()

if "history" not in st.session_state:
    st.session_state.history = []

for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)

q = st.chat_input("Ask about the company")
if q:
    st.chat_message("user").write(q)

    q_vec = embed([q], "RETRIEVAL_QUERY")
    hits = col.query(query_embeddings=q_vec, n_results=config.TOP_K)
    context = "\n\n".join(hits["documents"][0])
    pages = sorted({m["page"] for m in hits["metadatas"][0]})

    prompt = f"""You are a company assistant. Answer ONLY from the context below.
If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {q}"""

    with st.spinner("Thinking..."):
        answer = generate(prompt)

    st.chat_message("assistant").write(answer + f"\n\n*Sources: pages {pages}*")

    st.session_state.history += [("user", q), ("assistant", answer)]