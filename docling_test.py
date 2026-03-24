from docling.document_converter import DocumentConverter

source = "https://blog.mozilla.org/press-br/files/2013/10/Mozilla-Firefox_ReviewersGuide-FINAL-April-2014.pdf"
converter = DocumentConverter()
doc = converter.convert(source).document

with open("flamehamster.md", "w", encoding="utf-8") as f:
    f.write(doc.export_to_markdown())