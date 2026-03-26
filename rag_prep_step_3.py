import os
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone
import re
import time

load_dotenv()

def split_markdown_by_h1(md_text):
    pattern = r"(?m)^# .+?(?=^# |\Z)"
    chunks = re.findall(pattern, md_text, re.DOTALL)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
dense_index = pc.Index("gross-app")
data_dir = Path("data")
BATCH_SIZE = 96  # max number of records that Pinecone allows at once  

# Load and chunk all markdown files in the folder
for file_path in data_dir.glob("*.md"):
    records = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    chunks = split_markdown_by_h1(md_content)
    manual_name = file_path.stem  # Filename without extension

    for i, chunk in enumerate(chunks):
        records.append({
            "id": f"{manual_name}-chunk-{i}",
            "chunk_text": chunk,
            "manual": manual_name
        })

    time.sleep(90)  # to avoid rate limiting
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        dense_index.upsert_records("all-gross", batch)

print("Complete!")
