import csv
from pathlib import Path

import requests

books_dir = Path("books")
books_dir.mkdir(exist_ok=True)

with open("books.csv") as f:
    for row in csv.DictReader(f):
        url = row["pdf_url"]
        dest = books_dir / url.split("/")[-1]
        if dest.exists():
            print(f"skip {dest}")
            continue
        print(f"downloading {row['title']} -> {dest}")
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
