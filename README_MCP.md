# SWAT-Copilot MCP Server

Model Context Protocol (MCP) server for interacting with SWAT (Soil and Water Assessment Tool) model projects.

## Overview

The SWAT-Copilot MCP server enables AI assistants like Claude to:

- **Locate SWAT Projects**: Find and identify SWAT model projects in directory structures
- **Load and Analyze**: Load project files and extract metadata
- **Read Outputs**: Parse and interpret SWAT model output files
- **Perform Analysis**: Calculate statistics, water balance, and time series analysis
- **Visualize Data**: Generate plots and charts from model outputs
- **Answer Questions**: Provide context-aware responses about SWAT modeling

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd SWAT-Copilot

# Install in development mode
pip install -e ".[dev]"
```

### Running the MCP Server

#### Standalone Mode

```bash
# Run the MCP server
swat-mcp

# Or using Python module
python -m swat_copilot.integrations.mcp
```

#### With Claude Desktop

Add to your Claude Desktop MCP configuration:
- **macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "swat-copilot": {
      "command": "python",
      "args": ["-m", "swat_copilot.integrations.mcp"],
      "env": {
        "DEFAULT_SWAT_PROJECT_PATH": "/path/to/your/swat/projects",
        "SWAT_DOCS_PATH": "/path/to/SWAT-Copilot/docs/swat_documentation"
      }
    }
  }
}
```

**Note:** Set `SWAT_DOCS_PATH` to enable documentation search. See [Documentation Setup](QUICK_SETUP_DOCS.md) for details.

## Available Tools

### Project Management

#### `find_swat_projects`
Search for SWAT projects in a directory tree.

**Parameters:**
- `search_path` (string): Directory to search
- `max_depth` (integer): Maximum search depth (default: 3)

**Example:**
```json
{
  "search_path": "/home/user/swat_models",
  "max_depth": 3
}
```

#### `load_swat_project`
Load a SWAT project from a directory.

**Parameters:**
- `project_path` (string, required): Path to SWAT project directory

**Example:**
```json
{
  "project_path": "/home/user/swat_models/my_watershed"
}
```

### Information & Summary

#### `get_project_summary`
Get comprehensive summary of the loaded SWAT project.

**Returns:** Project metadata, file counts, configuration details

#### `get_output_summary`
Get summary of all output files and available variables.

**Returns:** List of output files with variables and data shapes

### Analysis Tools

#### `get_variable_statistics`
Calculate statistics for any SWAT output variable.

**Parameters:**
- `variable` (string, required): Variable name (e.g., "FLOW_OUT", "SED_OUT")
- `output_type` (string): Type of output - "reach", "subbasin", or "hru" (default: "reach")
- `spatial_id` (integer): Optional specific reach/subbasin/HRU ID

**Example:**
```json
{
  "variable": "FLOW_OUT",
  "output_type": "reach",
  "spatial_id": 5
}
```

#### `get_time_series`
Extract time series data for a variable.

**Parameters:**
- `variable` (string, required): Variable name
- `output_type` (string): Output type (default: "reach")
- `spatial_id` (integer): Optional spatial unit ID

#### `calculate_water_balance`
Calculate water balance components from outputs.

**Parameters:**
- `output_type` (string): Output type to use (default: "subbasin")

**Returns:** Dictionary with precipitation, runoff, ET, and other components

### Visualization

#### `plot_time_series`
Generate time series plot for a variable.

**Parameters:**
- `variable` (string, required): Variable name to plot
- `output_type` (string): Output type (default: "reach")
- `spatial_id` (integer): Optional spatial unit ID
- `title` (string): Custom plot title

**Returns:** Base64-encoded PNG image

#### `plot_comparison`
Create comparison plot for multiple variables.

**Parameters:**
- `variables` (array of strings, required): List of variables to compare
- `output_type` (string): Output type (default: "reach")

**Returns:** Base64-encoded PNG image

### Documentation Search

#### `search_documentation`
Search SWAT documentation for information about parameters, variables, or concepts.

**Parameters:**
- `query` (string, required): Search query (e.g., "CN2 parameter", "surface runoff calculation")
- `top_k` (integer): Number of results to return (default: 3, max: 10)

**Returns:** Relevant excerpts from SWAT manuals with source citations

**Example:**
```json
{
  "query": "What is the CN2 parameter?",
  "top_k": 3
}
```

**Note:** Requires `SWAT_DOCS_PATH` environment variable to be set and documentation index to be built. See [Documentation Setup](QUICK_SETUP_DOCS.md).

## Resources

The server exposes SWAT project data as MCP resources:

- `swat://project/{name}` - Loaded project metadata
- `swat://output/{type}` - Specific output file data (reach, subbasin, hru)

## Architecture

```
swat_copilot/
├── config/           # Configuration and settings
├── core/             # Domain models (SWATProject, SWATFile)
├── data_access/      # File readers and schemas
├── services/         # Business logic (analysis, summary)
├── integrations/
│   └── mcp/          # MCP server implementation
├── api/              # REST API (FastAPI)
├── cli/              # Command-line interface (Typer)
├── visualization/    # Plotting utilities
└── llm/              # LLM prompts and RAG
```

## Example Usage with AI

**User:** "Find all SWAT projects in my models directory"

**AI with MCP:**
```
Using tool: find_swat_projects
{
  "search_path": "/home/user/models",
  "max_depth": 2
}
```

**User:** "Load the watershed_2023 project and show me streamflow statistics"

**AI with MCP:**
```
1. Using tool: load_swat_project
   {"project_path": "/home/user/models/watershed_2023"}

2. Using tool: get_variable_statistics
   {"variable": "FLOW_OUT", "output_type": "reach"}
```

**User:** "Create a plot showing streamflow over time for reach 5"

**AI with MCP:**
```
Using tool: plot_time_series
{
  "variable": "FLOW_OUT",
  "output_type": "reach",
  "spatial_id": 5,
  "title": "Streamflow at Reach 5"
}
```

**User:** "What does the CN2 parameter control in SWAT?"

**AI with MCP:**
```
Using tool: search_documentation
{
  "query": "CN2 parameter",
  "top_k": 3
}
```

Returns documentation excerpts explaining that CN2 is the SCS runoff curve number for moisture condition II, with details on its range (35-98) and impact on surface runoff generation.

## Development

### Project Structure

The codebase follows a layered architecture:

1. **Config Layer**: Runtime configuration and settings
2. **Core Layer**: Domain models and business entities
3. **Data Access Layer**: File I/O and data parsing
4. **Services Layer**: Orchestration and business logic
5. **Integration Layer**: MCP server, API, CLI entry points
6. **Support Layers**: Visualization, LLM prompts, RAG

### Adding New Tools

To add a new MCP tool:

1. Add the tool definition in `server.py` `list_tools()` handler
2. Implement the tool handler in `call_tool()` handler
3. Create service methods in appropriate service class
4. Update documentation

### Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=swat_copilot

# Type checking
mypy src/
```

## Configuration

Configuration is managed through environment variables and `.env` file:

```bash
# Copy example env file
cp .env.example .env

# Edit with your settings
nano .env
```

Key settings:
- `DEFAULT_SWAT_PROJECT_PATH`: Default path to search for projects
- `LLM_PROVIDER`, `LLM_MODEL`: LLM configuration for enhanced features
- `MCP_TRANSPORT`: Transport protocol (stdio for Claude Desktop)

## Common SWAT Variables

### Reach Output (output.rch)
- `FLOW_OUT`: Streamflow leaving reach (m³/s)
- `SED_OUT`: Sediment loading (metric tons)
- `ORGN_OUT`: Organic nitrogen (kg N)
- `ORGP_OUT`: Organic phosphorus (kg P)
- `NO3_OUT`: Nitrate loading (kg N)
- `SOLP_OUT`: Soluble phosphorus (kg P)

### Subbasin Output (output.sub)
- `PRECIP`: Precipitation (mm)
- `SURQ`: Surface runoff (mm)
- `LATQ`: Lateral flow (mm)
- `GW_Q`: Groundwater flow (mm)
- `ET`: Evapotranspiration (mm)
- `PET`: Potential ET (mm)

### HRU Output (output.hru)
- `PRECIP`: Precipitation (mm)
- `SURQ`: Surface runoff (mm)
- `PERC`: Percolation (mm)
- `ET`: Evapotranspiration (mm)
- `SW`: Soil water content (mm)

## Troubleshooting

### MCP Server Not Starting
- Check that all dependencies are installed: `pip install -e .`
- Verify Python version >= 3.11
- Check logs for specific error messages

### Project Not Found
- Ensure the project directory contains `file.cio` (SWAT control file)
- Check file permissions
- Verify path is absolute, not relative

### Output Files Not Loading
- Confirm SWAT model has been run and outputs generated
- Check output file format compatibility
- Look for `output.rch`, `output.sub`, or `output.hru` files

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check documentation in `docs/` directory
- Review example notebooks in `notebooks/`

## Roadmap

Future enhancements:
- [ ] Calibration assistance tools
- [ ] Scenario comparison features
- [ ] Geospatial visualization with maps
- [ ] Parameter sensitivity analysis
- [ ] Batch processing capabilities
- [ ] Integration with SWAT+ models
- [x] Enhanced RAG with SWAT documentation - **COMPLETED**
- [ ] Multi-document search across research papers
- [ ] Citation and reference tracking
