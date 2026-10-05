from pathlib import Path

from markitdown import MarkItDown

md = MarkItDown()
out_dir = Path("books_text")
out_dir.mkdir(exist_ok=True)

for pdf in sorted(Path("books").glob("*.pdf")):
    dest = out_dir / f"{pdf.stem}.md"
    print(f"converting {pdf} -> {dest}")
    result = md.convert(str(pdf))
    dest.write_text(result.text_content, encoding="utf-8")
