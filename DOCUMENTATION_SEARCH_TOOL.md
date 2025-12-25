# Documentation Search Tool - MCP Integration

## Overview

The `search_documentation` tool has been added to the SWAT-Copilot MCP server, enabling Claude Desktop and other AI assistants to search through SWAT documentation and provide accurate, source-backed answers.

## What Was Added

### 1. MCP Tool: `search_documentation`

A new tool was added to the MCP server that allows AI assistants to search the indexed SWAT documentation.

**Location:** [src/swat_copilot/integrations/mcp/server.py](src/swat_copilot/integrations/mcp/server.py)

**Features:**
- Searches through indexed SWAT PDF documentation
- Returns relevant excerpts with source citations
- Configurable number of results (1-10)
- Formatted output with page numbers and source files

### 2. Implementation Details

**Initialization:**
- The MCP server checks for `SWAT_DOCS_PATH` environment variable
- If set, initializes the RAG system automatically
- Loads the documentation index from the specified path

**Search Process:**
1. User asks a question about SWAT
2. AI assistant calls `search_documentation` tool
3. RAG system searches vector database for relevant content
4. Returns top-k results with source information
5. AI formats the answer using the documentation context

## Usage

### In Claude Desktop Config

```json
{
  "mcpServers": {
    "swat-copilot": {
      "command": "python",
      "args": ["-m", "swat_copilot.integrations.mcp"],
      "cwd": "/path/to/SWAT-Copilot",
      "env": {
        "SWAT_DOCS_PATH": "/path/to/SWAT-Copilot/docs/swat_documentation"
      }
    }
  }
}
```

### Example Queries

**Query 1: Parameter Information**
```
User: "What is the CN2 parameter in SWAT?"

Claude uses: search_documentation("CN2 parameter", top_k=3)

Returns: Definitions, range (35-98), and impact on surface runoff
```

**Query 2: Calculation Methods**
```
User: "How does SWAT calculate surface runoff?"

Claude uses: search_documentation("surface runoff calculation", top_k=3)

Returns: SCS curve number method explanation and equations
```

**Query 3: Output Variables**
```
User: "What variables are available in output.rch?"

Claude uses: search_documentation("output.rch variables", top_k=5)

Returns: List of reach output variables with descriptions
```

## Tool Specification

### Input Schema

```json
{
  "query": {
    "type": "string",
    "required": true,
    "description": "Search query for SWAT documentation"
  },
  "top_k": {
    "type": "integer",
    "default": 3,
    "minimum": 1,
    "maximum": 10,
    "description": "Number of results to return"
  }
}
```

### Output Format

```markdown
# Documentation Search Results for: 'query'

Found N relevant excerpt(s):

## Result 1
**Source:** swat-io-documentation-2012.pdf
**Page:** 255

[Relevant text excerpt from documentation...]

--------------------------------------------------------------------------------

## Result 2
**Source:** swat-io-documentation-2012.pdf
**Page:** 246

[Another relevant excerpt...]
```

## Benefits

1. **Accurate Information**: Answers are grounded in official SWAT documentation
2. **Source Citations**: Every answer includes page numbers and source files
3. **Fast Search**: Vector similarity search returns results in < 1 second
4. **Contextual**: Retrieves relevant context, not just keyword matches
5. **Extensible**: Easy to add more documentation PDFs

## Current Capabilities

✅ **Indexed Documentation:**
- SWAT IO Documentation 2012 (6.9 MB, ~500 pages)

✅ **Searchable Topics:**
- Parameter definitions (CN2, ESCO, ALPHA_BF, etc.)
- Variable descriptions (FLOW_OUT, SED_OUT, etc.)
- Calculation methods (runoff, evapotranspiration, etc.)
- File formats (output.rch, output.sub, etc.)
- Input file specifications

## Adding More Documentation

To expand the searchable documentation:

1. **Add PDFs:**
   ```bash
   cp your-swat-manual.pdf docs/swat_documentation/pdfs/
   ```

2. **Rebuild Index:**
   ```bash
   python scripts/setup_documentation.py --yes
   ```

3. **Restart Claude Desktop**

4. **New content is now searchable!**

## Technical Architecture

```
User Question
     ↓
Claude Desktop
     ↓
MCP: search_documentation tool
     ↓
SWATRAGSystem.retrieve_context()
     ↓
SWATDocumentationIndex.search()
     ↓
ChromaDB vector similarity search
     ↓
Top-k relevant chunks
     ↓
Format with source citations
     ↓
Return to Claude
     ↓
AI generates answer with sources
```

## Files Modified

1. **[server.py](src/swat_copilot/integrations/mcp/server.py)**
   - Added `search_documentation` tool definition
   - Implemented `_search_documentation()` handler
   - Added RAG system initialization in `__init__()`

2. **[README_MCP.md](README_MCP.md)**
   - Documented the new tool
   - Added usage examples
   - Updated configuration instructions

3. **[doc_indexer.py](src/swat_copilot/llm/doc_indexer.py)**
   - Fixed import: `langchain.text_splitter` → `langchain_text_splitters`

## Performance

- **Index Size:** 14 MB for 6.9 MB PDF
- **Index Build Time:** ~14 seconds
- **Search Latency:** < 1 second per query
- **Memory Usage:** ~100 MB (embeddings model + index)

## Future Enhancements

- [ ] Support for markdown documentation files
- [ ] Add SWAT+ documentation
- [ ] Include research papers and technical reports
- [ ] Multi-language support
- [ ] Citation tracking and cross-referencing
- [ ] Semantic search improvements with reranking

## Troubleshooting

### Documentation Search Not Available

**Error:** "Documentation search not available"

**Solutions:**
1. Check `SWAT_DOCS_PATH` is set in Claude config
2. Verify path exists: `ls /path/to/docs/swat_documentation`
3. Check index exists: `ls /path/to/docs/swat_documentation/vector_index/`
4. Rebuild if needed: `python scripts/setup_documentation.py --yes`

### No Results Found

**Issue:** Search returns "No documentation found"

**Solutions:**
1. Try different search terms (e.g., "CN2" vs "curve number")
2. Increase `top_k` value for more results
3. Check if topic is covered in indexed PDFs
4. Add more documentation sources

### Import Errors

**Error:** "No module named 'langchain_text_splitters'"

**Solution:**
```bash
pip install langchain langchain-community chromadb pypdf sentence-transformers
```

## Example Session

```
User: What's the difference between SURQ and LATQ in SWAT?

Claude: Let me search the SWAT documentation for information about SURQ and LATQ.

[Uses search_documentation("SURQ LATQ difference")]

Based on the SWAT documentation:

**SURQ (Surface Runoff):**
- Represents overland flow to the main channel
- Calculated using SCS curve number method
- Occurs when precipitation exceeds infiltration capacity
- Units: mm H₂O

**LATQ (Lateral Flow):**
- Subsurface flow that moves laterally through soil layers
- Calculated using kinematic storage model
- Occurs in saturated zone above water table
- Units: mm H₂O

Source: SWAT IO Documentation 2012, pages 458-461
```

## Related Documentation

- [Quick Setup Guide](QUICK_SETUP_DOCS.md) - How to set up documentation indexing
- [Full Setup Guide](docs/DOCUMENTATION_SETUP.md) - Detailed documentation setup
- [MCP Server Docs](README_MCP.md) - All MCP tools and features
- [Verification Guide](docs/VERIFY_MCP_SETUP.md) - How to verify setup

---

**Status:** ✅ Implemented and tested (2025-12-25)

**Version:** SWAT-Copilot v0.0.1
