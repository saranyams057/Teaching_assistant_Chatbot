from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from embeddings import retriever
from prompts import RAG_QA_PROMPT

# ===============================
# CONFIG
# ===============================
VECTOR_DIR = "chroma_db"
COLLECTION_NAME = "multi_modal_rag"
TOP_K = 5

# ===============================
# LOAD VECTORSTORE
# ===============================
embeddings = OllamaEmbeddings(model="llava:7b")

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=VECTOR_DIR,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
# ====================================
# 1️⃣ PROMPT BUILDERS
# ====================================

def build_text_table_prompt(texts: list[str], tables: list[str], question: str) -> HumanMessage:
    """
    Prompt for text + table context
    """
    context = "\n\n".join(texts + tables)

    prompt = RAG_QA_PROMPT.format(
        context=context,
        question=question
    )
    return HumanMessage(content=prompt)


def build_image_prompt(image_b64_list: list[str], question: str) -> HumanMessage:
    """
    Prompt for images (base64 already available)
    """
    image_block = ""
    for i, img in enumerate(image_b64_list, 1):
        image_block += f"[Image {i}]: data:image/jpeg;base64,{img}\n"

    prompt = f"""
You are a vision-capable teacher AI.

Analyze the images below and answer the question.
Use only what is visible in the images.

{image_block}

Question:
{question}

Answer:
"""
    return HumanMessage(content=prompt)


# ====================================
# 2️⃣ MULTIMODAL RAG FUNCTION
# ====================================

def multimodal_rag_chain(question: str, top_k: int = 5):
    """
    Main RAG pipeline used by Streamlit UI
    """

    # -----------------------------
    # Retrieve documents
    # -----------------------------
    docs = retriever.invoke(question)

    text_context = []
    table_context = []
    image_context = []

    for doc in docs[:top_k]:
        modality = doc.metadata.get("type")

        if modality == "text":
            text_context.append(doc.page_content)

        elif modality == "table":
            table_context.append(doc.page_content)

        elif modality == "image":
            # page_content already contains image summary
            # raw base64 stored in metadata OR page_content depending on your setup
            image_context.append(doc.metadata.get("raw_content", doc.page_content))

    # -----------------------------
    # Ollama LLaVA model
    # -----------------------------
    llm = ChatOllama(
        model="llava:7b",
        temperature=0.2,
        max_tokens=512,
    )

    # -----------------------------
    # Text + Table reasoning
    # -----------------------------
    text_answer = ""
    if text_context or table_context:
        text_prompt = build_text_table_prompt(text_context, table_context, question)
        text_answer = llm.invoke([text_prompt]).content

    # -----------------------------
    # Image reasoning (optional)
    # -----------------------------
    image_answer = ""
    if image_context:
        image_prompt = build_image_prompt(image_context, question)
        image_answer = llm.invoke([image_prompt]).content

    # -----------------------------
    # Merge final answer
    # -----------------------------
    final_answer = text_answer

    if image_answer:
        final_answer += f"\n\n📷 **From Images:**\n{image_answer}"

    return {
        "answer": final_answer.strip(),
        "images": image_context
    }


