from pathlib import Path
from fastembed import TextEmbedding
import json
def index_project_texts(project_dir: Path, out_path: Path):
   emb = TextEmbedding()
   docs = []
   for p in project_dir.glob("**/*"):
       if p.is_file() and p.suffix.lower() in {".txt", ".cio", ".sub", ".hru", ".sol", ".rte", ".mgt"}:
           txt = p.read_text(errors="ignore")
           docs.append({"path": str(p), "text": txt})
   vectors = list(emb.embed([d["text"] for d in docs]))
   out = [{"path": d["path"], "vector": v.tolist()} for d, v in zip(docs, vectors)]
   out_path.parent.mkdir(parents=True, exist_ok=True)
   out_path.write_text(json.dumps(out))
