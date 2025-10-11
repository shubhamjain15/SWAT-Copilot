"""Embedding utilities for retrieval augmented generation."""
from __future__ import annotations

import json
from pathlib import Path

from fastembed import TextEmbedding


def index_project_texts(project_dir: Path, out_path: Path) -> None:
    """Generate embeddings for textual project files."""
    embedder = TextEmbedding()
    documents = []
    for path in project_dir.glob("**/*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".txt", ".cio", ".sub", ".hru", ".sol", ".rte", ".mgt"}:
            continue
        documents.append({"path": str(path), "text": path.read_text(errors="ignore")})

    vectors = list(embedder.embed([doc["text"] for doc in documents]))
    payload = [{"path": doc["path"], "vector": vector.tolist()} for doc, vector in zip(documents, vectors)]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload))
