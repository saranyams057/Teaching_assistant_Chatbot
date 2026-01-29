
import os
import json
import uuid
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from ingestion import (
    data_loader,
    parse_elements,
    summarize_texts_and_tables,
    summarize_images,
)

# ===============================
# CONFIG
# ===============================
PDF_PATHS = [
    "data/Class_10_Mathematics_English_Medium-2025_Edition-www.tntextbooks.in.pdf",
    "data/Class_10_Science_English_Medium-2024_Edition-www.tntextbooks.in.pdf",
]

VECTOR_DIR = "chroma_db"
CACHE_FILE = "data/cache.json"
IMAGE_DIR = "data/images"

os.makedirs("data", exist_ok=True)

# ===============================
# LOAD CACHE (PERMANENT)
# ===============================
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {
        "texts": {},
        "tables": {},
        "images": {},
    }

# ===============================
# VECTOR STORE
# ===============================
embeddings = OllamaEmbeddings(model="llava:7b")

vectorstore = Chroma(
    collection_name="multi_modal_rag",
    embedding_function=embeddings,
    persist_directory=VECTOR_DIR,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# ===============================
# EMBEDDING PIPELINE 
# ===============================
def run_embedding():

    for pdf_path in PDF_PATHS:
        print(f"\n📘 Processing PDF → {pdf_path}")

        for element_batch in data_loader(
            pdf_path,
            image_output_dir=IMAGE_DIR,
            pages_per_batch=25,
        ):
            parsed_items = list(parse_elements(element_batch))

            # ---------------------------
            # TEXTS & TABLES
            # ---------------------------
            new_text_table_items = [
                item for item in parsed_items
                if (item[0] and item[0] not in cache["texts"])
                or (item[1] and item[1] not in cache["tables"])
            ]

            if new_text_table_items:
                summaries = summarize_texts_and_tables(new_text_table_items)

                for (text, table, _), summary in zip(new_text_table_items, summaries):
                    doc_id = str(uuid.uuid4())

                    vectorstore.add_documents(
                        [
                            Document(
                                page_content=summary,
                                metadata={
                                    "doc_id": doc_id,
                                    "source": pdf_path,
                                    "type": "text" if text else "table",
                                },
                            )
                        ]
                    )

                    if text:
                        cache["texts"][text] = summary
                        print("✅ Added text chunk")
                    elif table:
                        cache["tables"][table] = summary
                        print("✅ Added table chunk")

            # ---------------------------
            # IMAGES
            # ---------------------------
            new_image_items = [
                item for item in parsed_items
                if item[2] and item[2] not in cache["images"]
            ]

            if new_image_items:
                image_summaries = summarize_images(new_image_items)

                for (_, _, img_path), summary in zip(new_image_items, image_summaries):
                    doc_id = str(uuid.uuid4())

                    vectorstore.add_documents(
                        [
                            Document(
                                page_content=summary,
                                metadata={
                                    "doc_id": doc_id,
                                    "source": pdf_path,
                                    "type": "image",
                                },
                            )
                        ]
                    )

                    cache["images"][img_path] = summary
                    print(f"🖼 Added image → {os.path.basename(img_path)}")

    # ===============================
    # SAVE CACHE 
    # ===============================
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

    print("\n✅ Embedding completed and cached permanently")



# ===============================
if __name__ == "__main__":
    run_embedding()
