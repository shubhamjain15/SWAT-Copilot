# Quick Setup: Add SWAT Documentation to Claude

## 3-Minute Setup

### Step 1: Install Dependencies (1 min)

```bash
cd D:\SWAT-Copilot
pip install langchain langchain-community chromadb pypdf sentence-transformers
```

### Step 2: Add Your PDFs (30 seconds)

1. Create folders:
   ```bash
   mkdir docs\swat_documentation\pdfs
   mkdir docs\swat_documentation\text
   ```

2. Copy your SWAT PDFs to `D:\SWAT-Copilot\docs\swat_documentation\pdfs\`

   Example:
   - SWAT_User_Manual.pdf
   - SWAT_IO_Documentation.pdf
   - Your research papers, guides, etc.

### Step 3: Build Index (2-10 min, depending on file size)

```bash
python scripts\setup_documentation.py
```

Press `y` when asked to build index.

### Step 4: Update Claude Config (30 seconds)

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

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

**Important:**
- Replace `C:\\Python311\\python.exe` with your Python path (run `where python` to find it)
- Use double backslashes `\\` in paths

### Step 5: Restart Claude Desktop

Close and reopen Claude Desktop completely.

## Test It

Ask Claude:
- "What does the CN2 parameter do in SWAT?"
- "Explain surface runoff calculation in SWAT"
- "What variables are in output.rch file?"

Claude will search your PDFs and give answers with sources!

## File Structure

```
D:\SWAT-Copilot\
└── docs\
    └── swat_documentation\
        ├── pdfs\              ← Put your PDFs here
        │   ├── Manual.pdf
        │   ├── Theory.pdf
        │   └── ...
        ├── text\              ← Optional text files
        │   └── variables.txt
        └── vector_index\      ← Created automatically
```

## Troubleshooting

**Import Error:**
```bash
pip install langchain langchain-community chromadb pypdf sentence-transformers
```

**No PDFs found:**
- Check files are in `D:\SWAT-Copilot\docs\swat_documentation\pdfs\`
- Use `dir D:\SWAT-Copilot\docs\swat_documentation\pdfs` to verify

**Claude doesn't see docs:**
- Make sure you added `SWAT_DOCS_PATH` to env in config
- Restart Claude Desktop
- Check Claude logs in `%APPDATA%\Claude\logs\`

## Adding More Docs Later

1. Add new PDFs to `docs\swat_documentation\pdfs\`
2. Run `python scripts\setup_documentation.py` again
3. Restart Claude

Done!

## Need More Help?

See full guide: `docs\DOCUMENTATION_SETUP.md`
