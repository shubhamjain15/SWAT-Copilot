## Adding SWAT Documentation for AI-Powered Q&A

This guide shows you how to add SWAT documentation (PDFs, manuals, papers) so Claude can answer questions using your documentation.

## Quick Start

### 1. Install Dependencies

```bash
cd D:\SWAT-Copilot

# Install RAG dependencies
pip install langchain langchain-community chromadb pypdf sentence-transformers
```

### 2. Add Your Documentation

Copy your SWAT PDFs to the documentation folder:

```
D:\SWAT-Copilot\docs\swat_documentation\
├── pdfs\
│   ├── SWAT_User_Manual.pdf
│   ├── SWAT_IO_Documentation.pdf
│   ├── SWAT_Theory_Manual.pdf
│   ├── Your_Custom_Guide.pdf
│   └── ...
└── text\
    ├── variables_list.txt
    ├── parameters_guide.txt
    └── ...
```

**Create the folders if they don't exist:**

```bash
mkdir docs\swat_documentation\pdfs
mkdir docs\swat_documentation\text
```

### 3. Build the Documentation Index

```bash
python scripts\setup_documentation.py
```

This will:
- Scan all PDFs and text files
- Extract and chunk the content
- Create vector embeddings
- Build a searchable database

**This takes 2-10 minutes depending on file size.**

### 4. Update MCP Configuration

Edit your Claude Desktop config to enable documentation path:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "swat-copilot": {
      "command": "C:\\Python311\\python.exe",
      "args": ["-m", "swat_copilot.integrations.mcp"],
      "cwd": "D:\\SWAT-Copilot",
      "env": {
        "SWAT_DOCS_PATH": "D:\\SWAT-Copilot\\docs\\swat_documentation"
      }
    }
  }
}
```

### 5. Restart Claude Desktop

Close and reopen Claude Desktop for changes to take effect.

### 6. Test It!

Ask Claude questions about SWAT:

```
"What does the CN2 parameter do in SWAT?"
"Explain the difference between SURQ and LATQ"
"How do I interpret sediment output values?"
"What's the water balance equation in SWAT?"
```

Claude will search your documentation and provide answers with sources!

## Advanced Usage

### Adding More Documentation

1. **Add new PDFs:**
   ```bash
   # Copy PDFs to docs folder
   copy C:\Downloads\*.pdf D:\SWAT-Copilot\docs\swat_documentation\pdfs\
   ```

2. **Rebuild index:**
   ```bash
   python scripts\setup_documentation.py
   ```

### Checking What's Indexed

```python
from pathlib import Path
from swat_copilot.llm.rag import SWATRAGSystem

# Initialize
docs_path = Path("D:/SWAT-Copilot/docs/swat_documentation")
rag = SWATRAGSystem(documentation_path=docs_path)

# Search
results = rag.retrieve_context("curve number", top_k=5)

for i, result in enumerate(results, 1):
    print(f"\n{i}. From: {result['source']}")
    print(f"   Page: {result.get('page', 'N/A')}")
    print(f"   Text: {result['text'][:200]}...")
```

### Using in Python Scripts

```python
from pathlib import Path
from swat_copilot.llm.rag import SWATRAGSystem
from swat_copilot.llm.prompts import PromptTemplates

# Load documentation
docs_path = Path("D:/SWAT-Copilot/docs/swat_documentation")
rag = SWATRAGSystem(documentation_path=docs_path)

# Search for context
query = "How does SWAT calculate surface runoff?"
context = rag.retrieve_context(query, top_k=3)

# Display results
for ctx in context:
    print(f"\nSource: {ctx['source']}")
    print(f"Content: {ctx['text']}\n")
    print("-" * 80)
```

## File Types Supported

### PDFs
- User manuals
- Theory documentation
- Research papers
- Technical reports
- Any PDF with selectable text

### Text Files (.txt)
- Variable definitions
- Parameter descriptions
- FAQ documents
- Custom guides

### Markdown (.md)
Add to `DirectoryLoader` in `doc_indexer.py`:
```python
md_loader = DirectoryLoader(
    str(docs_path / "markdown"),
    glob="**/*.md",
)
```

## Troubleshooting

### "No module named 'langchain'"

```bash
pip install langchain langchain-community chromadb pypdf sentence-transformers
```

### "No documents found"

Check that files are in the right place:
```bash
dir D:\SWAT-Copilot\docs\swat_documentation\pdfs
```

Should show your PDF files.

### "Index build failed"

1. Check PDF files aren't corrupted
2. Try with just 1-2 small PDFs first
3. Check Python can read the files:
   ```python
   from pathlib import Path
   pdf = Path("D:/SWAT-Copilot/docs/swat_documentation/pdfs/manual.pdf")
   print(pdf.exists())  # Should be True
   ```

### Documentation search returns no results

1. **Rebuild the index:**
   ```bash
   python scripts\setup_documentation.py
   ```

2. **Check index exists:**
   ```bash
   dir D:\SWAT-Copilot\docs\swat_documentation\vector_index
   ```

3. **Test manually:**
   ```python
   from pathlib import Path
   from swat_copilot.llm.rag import SWATRAGSystem

   rag = SWATRAGSystem(Path("D:/SWAT-Copilot/docs/swat_documentation"))
   results = rag.retrieve_context("test query")
   print(f"Found {len(results)} results")
   ```

## Performance Tips

### Large PDF Files

If you have very large PDFs (>100 MB):

1. **Split them into chapters:**
   - Use a PDF splitter tool
   - Put chapters in separate files

2. **Increase chunk size** in `doc_indexer.py`:
   ```python
   text_splitter = RecursiveCharacterTextSplitter(
       chunk_size=2000,  # Increased from 1000
       chunk_overlap=400,
   )
   ```

### Faster Indexing

Use a smaller embedding model in `doc_indexer.py`:
```python
self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"  # Faster, smaller
)
```

### Better Search Results

Increase `top_k` to get more context:
```python
results = rag.retrieve_context(query, top_k=5)  # Get top 5 instead of 3
```

## Example Documentation Structure

```
docs/swat_documentation/
├── pdfs/
│   ├── manuals/
│   │   ├── SWAT2012_User_Manual.pdf
│   │   ├── SWAT_IO_Documentation.pdf
│   │   └── SWAT_Theoretical_Documentation.pdf
│   ├── papers/
│   │   ├── Arnold_et_al_2012.pdf
│   │   ├── Neitsch_et_al_2011.pdf
│   │   └── ...
│   └── guides/
│       ├── Calibration_Guide.pdf
│       ├── GIS_Setup_Guide.pdf
│       └── ...
├── text/
│   ├── variables_reference.txt
│   ├── parameters_reference.txt
│   ├── file_formats.txt
│   └── faq.txt
└── vector_index/  (created automatically)
    └── [database files]
```

## Where to Get SWAT Documentation

1. **Official SWAT Website:**
   - https://swat.tamu.edu/documentation/
   - User manuals, IO docs, theory docs

2. **SWAT+ Documentation:**
   - https://swatplus.gitbook.io/

3. **Research Papers:**
   - Google Scholar: "SWAT model" + your topic
   - Save PDFs to documentation folder

4. **Your Own Notes:**
   - Create `.txt` files with your findings
   - Add project-specific information
   - Custom variable definitions

## Next Steps

1. **Add your PDFs** to `docs/swat_documentation/pdfs/`
2. **Run setup script:** `python scripts\setup_documentation.py`
3. **Update Claude config** with SWAT_DOCS_PATH
4. **Restart Claude Desktop**
5. **Start asking questions!**

Claude will now have access to all your SWAT documentation and can provide informed answers with citations!
