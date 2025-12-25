# What's New in SWAT-Copilot

## Latest Update: Documentation Search via MCP (2025-12-25)

### New Feature: `search_documentation` Tool

You can now ask Claude Desktop questions about SWAT directly, and it will search through your SWAT documentation to provide accurate, source-backed answers!

### What This Means For You

**Before:**
- Had to manually search through PDF manuals
- Difficult to find specific parameter definitions
- No quick way to look up variable meanings

**Now:**
- Ask Claude: "What is the CN2 parameter?"
- Get instant answers with page references
- Search across all your SWAT documentation at once

### Quick Example

```
You: "What does the CN2 parameter control in SWAT?"

Claude (using search_documentation):
CN2 is the SCS runoff curve number for moisture condition II.
It controls the amount of surface runoff generated in the model.

Range: 35-98
Higher values = more surface runoff
Lower values = more infiltration

Source: SWAT IO Documentation 2012, Page 255
```

### How to Use It

1. **Set up documentation** (one-time, already done for you):
   ```bash
   python scripts/setup_documentation.py --yes
   ```

2. **Update Claude Desktop config**:
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

3. **Restart Claude Desktop**

4. **Start asking questions!**

### What You Can Ask About

✅ **Parameters:**
- "What is CN2?"
- "Explain ESCO parameter"
- "What does ALPHA_BF control?"

✅ **Variables:**
- "What variables are in output.rch?"
- "What is FLOW_OUT?"
- "Difference between SURQ and LATQ?"

✅ **Calculations:**
- "How does SWAT calculate runoff?"
- "Explain evapotranspiration calculation"
- "What is the water balance equation?"

✅ **File Formats:**
- "What's in the .sub output file?"
- "How to read output.hru?"
- "What does file.cio contain?"

### Technical Details

**Indexed Documentation:**
- SWAT IO Documentation 2012 (6.9 MB)
- 500+ pages fully searchable
- Vector database for semantic search

**Performance:**
- Search time: < 1 second
- Accuracy: Retrieves relevant sections
- Citations: Includes page numbers and sources

**Under the Hood:**
- Uses ChromaDB for vector storage
- Sentence transformers for embeddings
- LangChain for document processing
- RAG (Retrieval Augmented Generation)

### All MCP Tools Available

With the MCP server running in Claude Desktop, you now have access to:

1. ✅ **find_swat_projects** - Locate SWAT projects on your system
2. ✅ **load_swat_project** - Load project files
3. ✅ **get_project_summary** - Get project overview
4. ✅ **get_output_summary** - Summarize outputs
5. ✅ **get_variable_statistics** - Calculate stats
6. ✅ **get_time_series** - Extract time series
7. ✅ **calculate_water_balance** - Water balance analysis
8. ✅ **plot_time_series** - Create time series plots
9. ✅ **plot_comparison** - Compare variables
10. ✅ **search_documentation** - 🆕 Search SWAT documentation

### Documentation & Guides

- [Quick Setup](QUICK_SETUP_DOCS.md) - 3-minute setup guide
- [Full Documentation Setup](docs/DOCUMENTATION_SETUP.md) - Detailed guide
- [MCP Server Documentation](README_MCP.md) - All tools and features
- [Verification Guide](docs/VERIFY_MCP_SETUP.md) - How to verify setup
- [Documentation Search Tool](DOCUMENTATION_SEARCH_TOOL.md) - Technical details
- [Setup Complete Summary](SETUP_COMPLETE.md) - What's been configured

### Next Steps

1. **Test the documentation search:**
   - Ask Claude about SWAT parameters
   - Try searching for calculation methods
   - Look up output variable definitions

2. **Add more documentation** (optional):
   - Copy more SWAT PDFs to `docs/swat_documentation/pdfs/`
   - Run `python scripts/setup_documentation.py --yes`
   - Restart Claude Desktop

3. **Explore other MCP tools:**
   - Find and load a SWAT project
   - Analyze model outputs
   - Create visualizations

### System Status

✅ **Documentation Index:** Built (14 MB, 1 PDF indexed)
✅ **RAG System:** Operational
✅ **MCP Server:** Updated with search tool
✅ **Tests:** Passing
✅ **Ready to Use:** Yes!

### Known Issues & Limitations

- ⚠️ Deprecation warnings for langchain classes (non-breaking)
- 📝 Only SWAT IO Documentation 2012 currently indexed
- 🔧 Requires `SWAT_DOCS_PATH` environment variable set

### Future Enhancements

Coming soon:
- [ ] More documentation sources (Theory Manual, User Guide)
- [ ] SWAT+ documentation support
- [ ] Research paper integration
- [ ] Citation tracking
- [ ] Multi-document cross-referencing

### Support

**Having issues?**
1. Check [Verification Guide](docs/VERIFY_MCP_SETUP.md)
2. Review Claude Desktop logs
3. Ensure `SWAT_DOCS_PATH` is set correctly
4. Verify index exists: `ls docs/swat_documentation/vector_index/`

**Everything working?**
Start exploring! Ask Claude anything about SWAT and watch it search through your documentation automatically.

---

**Version:** 0.0.1
**Last Updated:** 2025-12-25
**Environment:** Python 3.11, Linux (WSL/Container)
