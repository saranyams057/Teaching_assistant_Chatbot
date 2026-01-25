import streamlit as st
from rag_chatbot import multimodal_rag_chain

# ===============================
# 1️⃣ Page Config
# ===============================
st.set_page_config(
    page_title="📚 Teacher AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Teacher AI Assistant")
st.markdown(
    "Ask questions based on your textbooks. "
    "Answers are generated using text, tables, and image summaries."
)

# ===============================
# 2️⃣ Session State (Chat Memory)
# ===============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ===============================
# 3️⃣ Clear Chat Button
# ===============================
col1, col2 = st.columns([1, 5])

with col1:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ===============================
# 4️⃣ Display Chat History
# ===============================
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===============================
# 5️⃣ User Input (Chat Style)
# ===============================
user_input = st.chat_input("Ask a question from the textbook...")

# ===============================
# 6️⃣ RAG Execution
# ===============================
if user_input:
    # Show user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Run RAG
    with st.chat_message("assistant"):
        with st.spinner("📖 Thinking..."):
            try:
                answer = multimodal_rag_chain(user_input)
            except Exception as e:
                answer = f"❌ Error: {e}"

        st.markdown(answer)

    # Save assistant response
    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )
