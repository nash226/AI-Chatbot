import os
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone
import re
import time

load_dotenv()

INDEX_NAME = "gross-app"
NAMESPACE = "all-gross"

def split_markdown_by_h1(md_text):
    pattern = r"(?m)^# .+?(?=^# |\Z)"
    chunks = re.findall(pattern, md_text, re.DOTALL)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
if not pc.has_index(INDEX_NAME):
    print(f"Creating Pinecone index: {INDEX_NAME}")
    pc.create_index_for_model(
        name=INDEX_NAME,
        cloud="aws",
        region="us-east-1",
        embed={
            "model": "llama-text-embed-v2",
            "field_map": {"text": "chunk_text"},
        },
    )

dense_index = pc.Index(INDEX_NAME)
project_root = Path(__file__).resolve().parent
data_dir = project_root / "code" / "evals" / "data"
BATCH_SIZE = 96  # max number of records that Pinecone allows at once  

if not data_dir.exists():
    raise FileNotFoundError(f"Expected markdown data folder at {data_dir}")

markdown_files = sorted(data_dir.glob("*.md"))
if not markdown_files:
    raise FileNotFoundError(f"No markdown files found in {data_dir}")

print(f"Loading {len(markdown_files)} markdown files from {data_dir}")

# Load and chunk all markdown files in the folder
for file_path in markdown_files:
    records = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    chunks = split_markdown_by_h1(md_content)
    manual_name = file_path.stem  # Filename without extension
    print(f"Preparing {manual_name}: {len(chunks)} chunks")

    for i, chunk in enumerate(chunks):
        records.append({
            "id": f"{manual_name}-chunk-{i}",
            "chunk_text": chunk,
            "manual": manual_name
        })

    time.sleep(90)  # to avoid rate limiting
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        dense_index.upsert_records(NAMESPACE, batch)

print("Complete!")
