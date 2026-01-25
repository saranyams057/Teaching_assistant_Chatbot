import os
import warnings
import base64
from typing import List, Generator, Tuple
# NEW import
from prompts import TEXT_TABLE_SUMMARY_PROMPT, IMAGE_SUMMARY_INSTRUCTION
from dotenv import load_dotenv
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import (
    Element,
    NarrativeText,
    Title,
    Table,
    Image,
    CompositeElement,
)

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# =======================================
# SETUP
# =======================================
warnings.filterwarnings("ignore")
load_dotenv()

print("🚀 Memory-efficient RAG ingestion started")


# =======================================
# 1️⃣ PAGE-WISE PDF LOADER
# =======================================
def data_loader(
    pdf_path: str,
    image_output_dir: str = "data/images",
    pages_per_batch: int = 25,
) -> Generator[List[Element], None, None]:

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ PDF not found: {pdf_path}")

    os.makedirs(image_output_dir, exist_ok=True)

    page_offset = 0
    print(f"\n📘 Loading PDF: {pdf_path}")

    while True:
        print(f"📄 Pages {page_offset + 1} → {page_offset + pages_per_batch}")

        elements = partition_pdf(
            filename=pdf_path,
            strategy="hi_res",
            infer_table_structure=True,
            extract_images_in_pdf=True,
            image_output_dir_path=image_output_dir,
            chunking_strategy="by_title",
            max_characters=10000,
            combine_text_under_n_chars=2000,
            new_after_n_chars=6000,
            max_pages=pages_per_batch,
            page_offset=page_offset,
        )

        if not elements:
            break

        yield elements
        page_offset += pages_per_batch


# =======================================
# 2️⃣ STREAMING ELEMENT PARSER
# =======================================
def parse_elements(
    elements: List[Element],
) -> Generator[Tuple[str | None, str | None, str | None], None, None]:

    for el in elements:
        sub_elements = (
            el.metadata.orig_elements if isinstance(el, CompositeElement) else [el]
        )

        for sub_el in sub_elements:

            if isinstance(sub_el, (NarrativeText, Title)) and sub_el.text:
                yield sub_el.text.strip(), None, None

            elif isinstance(sub_el, Table) and sub_el.text:
                yield None, sub_el.text.strip(), None

            elif isinstance(sub_el, Image):
                img_path = getattr(sub_el.metadata, "image_path", None)
                if img_path and os.path.exists(img_path):
                    yield None, None, img_path


# =======================================
# 3️⃣ TEXT & TABLE SUMMARIZATION (BATCHED)
# =======================================
def summarize_texts_and_tables(
    content_items: List[Tuple[str | None, str | None, str | None]],
    batch_size: int = 8,
) -> List[str]:

    llm = ChatOllama(model="llava:7b", temperature=0)


    chain = TEXT_TABLE_SUMMARY_PROMPT | llm | StrOutputParser()
    summaries = []

    buffer = []

    for text, table, _ in content_items:
        content = text or table
        if not content:
            continue

        buffer.append(content)

        if len(buffer) >= batch_size:
            for item in buffer:
                summaries.append(chain.invoke(item))
            buffer.clear()

    for item in buffer:
        summaries.append(chain.invoke(item))

    return summaries


# =======================================
# 4️⃣ IMAGE SUMMARIZATION (LLAVA)
# =======================================
def summarize_images(
    content_items: List[Tuple[str | None, str | None, str | None]]
) -> List[str]:

    vision_llm = ChatOllama(model="llava:7b", temperature=0)
    image_summaries = []

    for _, _, img_path in content_items:
        if not img_path:
            continue

        try:
            with open(img_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode("utf-8")

            response = vision_llm.invoke(
                [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": IMAGE_SUMMARY_INSTRUCTION,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_b64}"
                                },
                            },
                        ],
                    }
                ]
            )

            image_summaries.append(response.content)

        except Exception as e:
            print(f"❌ Image failed: {e}")

    return image_summaries


# =======================================
# 5️⃣ MAIN PIPELINE (MULTI-PDF SAFE)
# =======================================
def ingest_pdfs(pdf_paths: List[str]):

    all_text_summaries = []
    all_image_summaries = []

    for pdf_path in pdf_paths:
        print(f"\n📚 Processing PDF → {pdf_path}")

        for element_batch in data_loader(pdf_path):

            parsed_items = list(parse_elements(element_batch))

            text_table_summaries = summarize_texts_and_tables(parsed_items)
            image_summaries = summarize_images(parsed_items)

            # 👉 Here is where you push to vector DB
            all_text_summaries.extend(text_table_summaries)
            all_image_summaries.extend(image_summaries)

    print("\n✅ Ingestion complete")
    print(f"📝 Text/Table summaries: {len(all_text_summaries)}")
    print(f"🖼 Image summaries: {len(all_image_summaries)}")

    return all_text_summaries, all_image_summaries




