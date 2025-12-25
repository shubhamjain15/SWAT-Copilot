# How to Verify Claude Desktop MCP Setup

## Method 1: Check Claude Desktop UI (Easiest)

1. **Open Claude Desktop**
2. **Look for the MCP indicator** in the bottom-right corner of the chat interface
   - You should see a small icon (usually looks like a puzzle piece or tool icon)
   - If the MCP server is loaded, it will show "swat-copilot" when you hover over it
3. **Click the MCP icon** to see available tools
   - Should show 9 tools: find_swat_projects, load_swat_project, get_project_summary, etc.

## Method 2: Try Using an MCP Tool

In Claude Desktop, try asking:

```
Can you list the available MCP tools?
```

or

```
Find SWAT projects in D:\Models
```

If the MCP server is working, Claude will:
- See the `find_swat_projects` tool
- Ask to use it
- Execute the search

## Method 3: Check Claude Desktop Logs

### Windows:
1. **Open File Explorer**
2. **Navigate to:** `%APPDATA%\Claude\logs\`
   - Or paste this in the address bar: `C:\Users\YOUR_USERNAME\AppData\Roaming\Claude\logs\`
3. **Open the most recent log file** (sorted by date)
4. **Search for:** `swat-copilot`

**What to look for:**
- ✅ **Success:** `[MCP] Connected to server: swat-copilot`
- ✅ **Success:** `[MCP] Loaded tools from swat-copilot`
- ❌ **Error:** `[MCP] Failed to start server: swat-copilot`
- ❌ **Error:** `[MCP] Error connecting to swat-copilot`

### Linux/macOS:
```bash
# Check logs
cat ~/.config/Claude/logs/mcp.log | grep swat-copilot

# Or tail the log file
tail -f ~/.config/Claude/logs/mcp.log
```

## Method 4: Verify Config File

### Windows:
1. **Open:** `%APPDATA%\Claude\claude_desktop_config.json`
   - Full path: `C:\Users\YOUR_USERNAME\AppData\Roaming\Claude\claude_desktop_config.json`

2. **Verify it looks like this:**
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

3. **Check for:**
   - ✅ Valid JSON syntax (no missing commas, brackets)
   - ✅ Double backslashes in Windows paths: `C:\\Python311\\python.exe`
   - ✅ Correct Python path (run `where python` in CMD to verify)
   - ✅ Correct project path

### Linux/macOS:
```bash
# View config
cat ~/.config/Claude/claude_desktop_config.json

# Verify JSON is valid
python -m json.tool ~/.config/Claude/claude_desktop_config.json
```

## Method 5: Test Python Path Manually

**Before restarting Claude Desktop**, verify the command works:

### Windows:
```cmd
cd D:\SWAT-Copilot
C:\Python311\python.exe -m swat_copilot.integrations.mcp
```

### Linux:
```bash
cd /workspaces/SWAT-Copilot
/opt/conda/bin/python -m swat_copilot.integrations.mcp
```

**Expected behavior:**
- The MCP server should start (may show initialization messages)
- It will wait for input from Claude Desktop
- Press `Ctrl+C` to stop it

**If you get errors:**
- ❌ `No module named 'swat_copilot'` → Package not installed, run `pip install -e .`
- ❌ `python: command not found` → Wrong Python path in config
- ❌ `ModuleNotFoundError: No module named 'mcp'` → Install MCP SDK: `pip install mcp`

## Method 6: Check MCP Server Status in Claude

Ask Claude directly:

```
What MCP servers are currently connected?
```

or

```
Show me the available tools
```

Claude will list all connected MCP servers and their tools.

## Common Issues and Fixes

### Issue 1: Config File Not Found
**Symptom:** Claude Desktop doesn't show MCP tools

**Fix:**
1. Create the config directory:
   ```cmd
   mkdir %APPDATA%\Claude
   ```
2. Create the config file manually:
   - Open Notepad
   - Paste the JSON config
   - Save as `claude_desktop_config.json` in `%APPDATA%\Claude\`
   - Make sure it's not saved as `.json.txt`

### Issue 2: Invalid JSON
**Symptom:** Claude Desktop doesn't start or crashes

**Fix:**
1. Validate JSON at https://jsonlint.com/
2. Common mistakes:
   - Missing comma between entries
   - Single backslashes in Windows paths (use `\\`)
   - Trailing commas
   - Missing quotes around strings

### Issue 3: Wrong Python Path
**Symptom:** Logs show "command not found" or "failed to start"

**Fix:**
```cmd
# Find your Python path
where python

# Or for Python 3 specifically
where python3

# Test the full path
"C:\Python311\python.exe" --version
```

Update the config with the correct path.

### Issue 4: Module Not Found
**Symptom:** Logs show "No module named 'swat_copilot'"

**Fix:**
```bash
# Navigate to project directory
cd D:\SWAT-Copilot

# Install in editable mode
pip install -e .

# Verify installation
python -c "import swat_copilot; print(swat_copilot.__version__)"
```

### Issue 5: Documentation Path Not Working
**Symptom:** Documentation search doesn't return results

**Fix:**
1. Verify the index exists:
   ```cmd
   dir D:\SWAT-Copilot\docs\swat_documentation\vector_index
   ```
2. If missing, rebuild:
   ```cmd
   python scripts\setup_documentation.py --yes
   ```
3. Update `SWAT_DOCS_PATH` in config to match actual location

## Quick Verification Checklist

- [ ] Claude Desktop config file exists at `%APPDATA%\Claude\claude_desktop_config.json`
- [ ] JSON syntax is valid (no errors when opening in text editor)
- [ ] Python path is correct (run `where python` to verify)
- [ ] SWAT-Copilot path is correct
- [ ] swat_copilot package is installed (`pip list | grep swat-copilot`)
- [ ] MCP SDK is installed (`pip list | grep mcp`)
- [ ] Documentation index exists (`docs\swat_documentation\vector_index\`)
- [ ] Claude Desktop has been completely closed and reopened
- [ ] MCP icon appears in Claude Desktop UI
- [ ] Can see swat-copilot in list of connected servers

## Testing the Full Setup

Once you've verified everything is working, test with these questions in Claude Desktop:

### Test 1: Documentation Search
```
What is the CN2 parameter in SWAT?
```

**Expected:** Claude searches your documentation and provides answer with page references.

### Test 2: Project Discovery
```
Find SWAT projects in D:\Models
```

**Expected:** Claude uses `find_swat_projects` tool to search for projects.

### Test 3: Project Analysis
```
Load the SWAT project at D:\Models\MyProject and give me a summary
```

**Expected:** Claude loads the project and provides overview.

### Test 4: Data Visualization
```
Plot the streamflow time series for reach 1
```

**Expected:** Claude extracts data and creates a plot.

## Still Having Issues?

1. **Check the exact error message** in Claude Desktop logs
2. **Test the Python command manually** from terminal
3. **Verify all paths** are absolute, not relative
4. **Ensure no typos** in the config file
5. **Try with minimal config first**, then add features

**Minimal working config:**
```json
{
  "mcpServers": {
    "swat-copilot": {
      "command": "C:\\Python311\\python.exe",
      "args": ["-m", "swat_copilot.integrations.mcp"],
      "cwd": "D:\\SWAT-Copilot"
    }
  }
}
```

Add `SWAT_DOCS_PATH` only after the basic MCP server is working.

---

**Need more help?** Check the logs first - they usually contain the exact error message that explains what went wrong.
