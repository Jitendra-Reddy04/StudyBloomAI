import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

_model = None


def embedder():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return _model


class VectorStore:
    """
    In-memory FAISS vector store with
    keyword + semantic search.
    """

    def __init__(self, chunks):
        self.chunks = chunks

        texts = [c["text"] for c in chunks]

        vecs = embedder().encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        self.index = faiss.IndexFlatIP(vecs.shape[1])

        self.index.add(
            np.asarray(vecs, dtype="float32")
        )

    def search(self, query, k=4):

        if not self.chunks:
            return []

        # -------------------------
        # 1. Semantic search
        # -------------------------

        q = embedder().encode(
            [query],
            normalize_embeddings=True
        )

        scores, ids = self.index.search(
            np.asarray(q, dtype="float32"),
            min(k, len(self.chunks))
        )

        semantic_results = []

        for score, idx in zip(scores[0], ids[0]):

            if idx >= 0:

                semantic_results.append(
                    {
                        **self.chunks[idx],
                        "score": float(score),
                        "keyword_match": False
                    }
                )

        # -------------------------
        # 2. Keyword search
        # -------------------------

        query_words = (
            query.lower()
            .replace("?", "")
            .replace(",", "")
            .replace(".", "")
            .split()
        )

        keyword_results = []

        for chunk in self.chunks:

            text = chunk["text"].lower()

            matched_words = []

            for word in query_words:

                if len(word) > 3 and word in text:
                    matched_words.append(word)

            if matched_words:

                keyword_results.append(
                    {
                        **chunk,
                        "score": 1.0,
                        "keyword_match": True,
                        "match_count": len(matched_words)
                    }
                )

        # -------------------------
        # 3. Combine results
        # -------------------------

        combined = {}

        for result in semantic_results:

            combined[result["text"]] = result

        for result in keyword_results:

            text = result["text"]

            if text in combined:

                # Exact keyword match gets priority
                combined[text]["score"] = 1.0
                combined[text]["keyword_match"] = True
                combined[text]["match_count"] = result["match_count"]

            else:

                combined[text] = result

        results = list(combined.values())

        # -------------------------
        # 4. Sort
        # -------------------------

        results.sort(
            key=lambda x: (
                x.get("keyword_match", False),
                x.get("match_count", 0),
                x.get("score", 0)
            ),
            reverse=True
        )

        # -------------------------
        # 5. Return top results


        return results[:k]
    