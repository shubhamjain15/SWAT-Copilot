# SWAT-Copilot

LLM-assisted exploration, QA, and visualization for SWAT projects.

## Project Status

This repository is an **active and ongoing effort**. Features and APIs are under continuous development — expect breaking changes until the first stable release.

## Features

- **MCP Server**: Model Context Protocol server for AI assistants (Claude, etc.)
- **Project Discovery**: Automatically find and load SWAT projects
- **Output Analysis**: Parse and analyze SWAT model outputs (reach, subbasin, HRU)
- **Visualization**: Generate plots and charts from model data
- **REST API**: FastAPI-based web service
- **CLI**: Command-line interface for quick analysis
- **Water Balance**: Calculate and validate water budget components
- **Time Series Analysis**: Extract and analyze temporal data
- **Extensible**: Modular architecture for easy customization

## Repository Layout

```
SWAT-Copilot/
├── src/swat_copilot/
│   ├── config/              # Configuration and settings
│   ├── core/                # Domain models (SWATProject, SWATFile)
│   ├── data_access/         # File readers and schemas
│   ├── services/            # Business logic (analysis, summary)
│   ├── integrations/
│   │   └── mcp/             # MCP server implementation
│   ├── api/                 # REST API (FastAPI)
│   ├── cli/                 # Command-line interface (Typer)
│   ├── visualization/       # Plotting utilities (Matplotlib)
│   └── llm/                 # LLM prompts and RAG
├── tests/                   # Unit and integration tests
├── docs/                    # Documentation
├── examples/                # Usage examples
└── notebooks/               # Jupyter notebooks
```

This layered structure separates the domain logic (`core`), data access primitives (`data_access`), and orchestration services (`services`). API and CLI entry points sit on top of those layers, with visualization and LLM helpers providing supporting capabilities.

## Quickstart

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd SWAT-Copilot

# Install the package
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

**Command-Line Interface:**
```bash
# Find SWAT projects
swat-copilot find /path/to/models

# Load and summarize a project
swat-copilot load /path/to/project
swat-copilot summary

# Analyze variables
swat-copilot stats FLOW_OUT --output-type reach

# Start MCP server
swat-copilot serve-mcp
```

**Python API:**
```python
from pathlib import Path
from swat_copilot.services.project_manager import ProjectManager
from swat_copilot.services.analysis import AnalysisService

# Load a SWAT project
manager = ProjectManager()
project = manager.load_project(Path("/path/to/project"))

# Analyze outputs
analyzer = AnalysisService(project)
stats = analyzer.get_variable_statistics("FLOW_OUT", "reach")
print(f"Mean flow: {stats['mean']:.2f} m³/s")
```

**MCP Server with Claude:**

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "swat-copilot": {
      "command": "python",
      "args": ["-m", "swat_copilot.integrations.mcp"]
    }
  }
}
```

### Development with Dev Containers

- Open the folder in **VS Code**
- Use the **Dev Containers** extension → *Reopen in Container*
- Once the container is built, you'll have Python, Jupyter, and geospatial libraries pre-installed and ready

## Documentation

- [Getting Started Guide](docs/GETTING_STARTED.md) - Installation and basic usage
- [MCP Server Documentation](README_MCP.md) - Model Context Protocol server details
- [Architecture Overview](docs/architecture.md) - System design and structure
- [API Reference](http://localhost:8000/docs) - REST API documentation (when server running)

## Contributing

Contributions are welcome! To propose a change:

1. Fork the repository.
2. Create a feature branch from `dev`:
   ```bash
   git checkout dev
   git checkout -b feature/<short-feature-name>
   ```
3. Commit your changes and open a pull request.
