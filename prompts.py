from langchain_core.prompts import PromptTemplate

# ===============================
# TEXT / TABLE SUMMARIZATION
# ===============================
TEXT_TABLE_SUMMARY_PROMPT = PromptTemplate(
    input_variables=["content"],
    template=(
        "You are a school teaching assistant.\n"
        "Summarize clearly with key facts, definitions, and explanations.\n\n"
        "{content}"
    ),
)

# ===============================
# IMAGE SUMMARIZATION
# ===============================
IMAGE_SUMMARY_INSTRUCTION = (
    "Describe this image for a school textbook. "
    "Focus on what is shown and its educational relevance."
)

# ===============================
# RAG QA PROMPT
# ===============================
RAG_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a school teaching assistant.\n\n"
        "Use ONLY the provided context to answer the question.\n"
        "If the answer is not present, say:\n"
        "\"I don't have enough information from the book.\"\n\n"
        "Context:\n"
        "{context}\n\n"
        "Question:\n"
        "{question}\n\n"
        "Answer clearly and concisely:"
    ),
)
