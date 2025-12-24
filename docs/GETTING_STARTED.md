# Getting Started with SWAT-Copilot

This guide will help you get started with SWAT-Copilot, an MCP server for analyzing SWAT (Soil and Water Assessment Tool) model projects.

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git (for cloning the repository)

### Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd SWAT-Copilot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### 1. Command-Line Interface

The CLI provides quick access to SWAT project analysis:

```bash
# Find SWAT projects in a directory
swat-copilot find /path/to/models

# Load a project
swat-copilot load /path/to/models/my_watershed

# Get project summary
swat-copilot summary

# Get output summary
swat-copilot outputs

# Calculate statistics for a variable
swat-copilot stats FLOW_OUT --output-type reach

# Start MCP server
swat-copilot serve-mcp
```

### 2. Python API

Use SWAT-Copilot as a Python library:

```python
from pathlib import Path
from swat_copilot.services.project_manager import ProjectManager
from swat_copilot.services.analysis import AnalysisService

# Initialize project manager
manager = ProjectManager()

# Find projects
projects = manager.find_projects(Path("/path/to/models"))

# Load a project
project = manager.load_project(projects[0])

# Analyze outputs
analyzer = AnalysisService(project)
stats = analyzer.get_variable_statistics("FLOW_OUT", "reach")
print(f"Mean flow: {stats['mean']:.2f}")
```

### 3. MCP Server

Use with AI assistants like Claude:

```bash
# Start the MCP server
python -m swat_copilot.integrations.mcp
```

Or configure in Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "swat-copilot": {
      "command": "python",
      "args": ["-m", "swat_copilot.integrations.mcp"],
      "env": {
        "DEFAULT_SWAT_PROJECT_PATH": "/path/to/swat/projects"
      }
    }
  }
}
```

### 4. REST API

Start the FastAPI server:

```bash
# Using uvicorn directly
uvicorn swat_copilot.api.app:app --reload

# Or via the module
python -m uvicorn swat_copilot.api.app:app --reload
```

Access the API:
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
DEFAULT_SWAT_PROJECT_PATH=/path/to/your/swat/projects
OPENAI_API_KEY=sk-...  # Optional, for LLM features
LOG_LEVEL=INFO
```

## Project Structure

A valid SWAT project must contain:
- `file.cio` - Control file (required)
- Input files (`.sub`, `.hru`, `.rte`, etc.)
- Output files (optional): `output.rch`, `output.sub`, `output.hru`

Example structure:
```
my_watershed/
├── file.cio
├── *.sub (subbasin files)
├── *.hru (HRU files)
├── *.rte (routing files)
├── output.rch (reach outputs)
├── output.sub (subbasin outputs)
└── output.hru (HRU outputs)
```

## Common Tasks

### Finding and Loading Projects

```python
from pathlib import Path
from swat_copilot.services.project_manager import ProjectManager

manager = ProjectManager()

# Find all SWAT projects in a directory tree
projects = manager.find_projects(Path("/models"), max_depth=3)

# Validate a project
validation = manager.validate_project(Path("/models/watershed_1"))
print(f"Valid: {validation['is_valid']}")

# Load project
project = manager.load_project(Path("/models/watershed_1"))
```

### Analyzing Outputs

```python
from swat_copilot.services.analysis import AnalysisService

analyzer = AnalysisService(project)

# Get variable statistics
stats = analyzer.get_variable_statistics(
    variable="FLOW_OUT",
    output_type="reach",
    spatial_id=5  # Optional: specific reach
)

# Get time series
ts = analyzer.get_time_series(
    variable="FLOW_OUT",
    output_type="reach"
)

# Calculate water balance
balance = analyzer.calculate_water_balance("subbasin")
```

### Creating Visualizations

```python
from swat_copilot.visualization.plots import SWATPlotter

plotter = SWATPlotter(project)

# Time series plot
image_data = plotter.plot_time_series(
    variable="FLOW_OUT",
    output_type="reach",
    spatial_id=5,
    title="Streamflow at Reach 5"
)

# Multiple variables
image_data = plotter.plot_comparison(
    variables=["FLOW_OUT", "SED_OUT"],
    output_type="reach"
)

# Distribution
image_data = plotter.plot_distribution(
    variable="FLOW_OUT",
    output_type="reach"
)

# Scatter plot
image_data = plotter.plot_scatter(
    x_variable="PRECIP",
    y_variable="FLOW_OUT",
    output_type="subbasin"
)
```

## Next Steps

- Read [README_MCP.md](../README_MCP.md) for MCP server details
- Explore example scripts in [examples/](../examples/)
- Check out the architecture in [docs/architecture.md](architecture.md)
- Review API documentation at `/docs` endpoint

## Troubleshooting

### "No project loaded" Error
Make sure to load a project first:
```python
manager.load_project(Path("/path/to/project"))
```

### "Variable not found" Error
Check available variables:
```python
from swat_copilot.services.summary import SummarizeService
summarizer = SummarizeService(project)
summary = summarizer.get_output_summary()
print(summary['variables'])
```

### Import Errors
Ensure the package is installed:
```bash
pip install -e .
```

## Support

- GitHub Issues: Report bugs and request features
- Documentation: Check `docs/` directory
- Examples: See `examples/` directory
