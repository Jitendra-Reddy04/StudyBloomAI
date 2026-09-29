from pypdf import PdfReader


def load_pdf(file, name):
    """Return one record per page: {source, page, text}."""
    reader = PdfReader(file)
    return [{"source": name, "page": i + 1, "text": p.extract_text() or ""} for i, p in enumerate(reader.pages)]


def chunk_pages(pages, size=200, overlap=40):
    """Split each page into overlapping word chunks, keeping source + page for citations."""
    chunks, step = [], max(size - overlap, 1)
    for p in pages:
        words = p["text"].split()
        for s in range(0, len(words), step):
            piece = " ".join(words[s:s + size])
            if len(piece.split()) >= 10:
                chunks.append({"source": p["source"], "page": p["page"], "text": piece})
            if s + size >= len(words):
                break
    return chunks