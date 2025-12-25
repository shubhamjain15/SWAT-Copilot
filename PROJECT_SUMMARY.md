# SWAT-Copilot Project Summary

This document provides an overview of the complete SWAT-Copilot MCP server implementation.

## 🎯 Project Overview

**SWAT-Copilot** is a Model Context Protocol (MCP) server that enables AI assistants to interact with SWAT (Soil and Water Assessment Tool) model projects. It provides tools for:

- Finding and loading SWAT projects
- Reading and parsing model inputs/outputs
- Performing hydrological analysis
- Generating visualizations
- Answering questions about model results

## 📁 Complete File Structure

```
SWAT-Copilot/
├── src/swat_copilot/
│   ├── __init__.py                          # Package initialization
│   ├── __main__.py                          # CLI entry point
│   │
│   ├── config/                              # Configuration Layer
│   │   ├── __init__.py
│   │   └── settings.py                      # Environment settings with Pydantic
│   │
│   ├── core/                                # Domain Layer
│   │   ├── __init__.py
│   │   └── projects.py                      # SWATProject, SWATFile, SWATProjectLocator
│   │
│   ├── data_access/                         # Data Access Layer
│   │   ├── __init__.py
│   │   ├── readers.py                       # File readers (Output, Control, etc.)
│   │   └── schemas.py                       # Data schemas (OutputData, WaterBalance)
│   │
│   ├── services/                            # Service Layer
│   │   ├── __init__.py
│   │   ├── project_manager.py               # Project lifecycle management
│   │   ├── summary.py                       # Summary generation
│   │   └── analysis.py                      # Statistical analysis
│   │
│   ├── integrations/mcp/                    # MCP Server
│   │   ├── __init__.py
│   │   ├── __main__.py                      # MCP entry point
│   │   └── server.py                        # MCP server implementation (9 tools)
│   │
│   ├── api/                                 # REST API (FastAPI)
│   │   ├── __init__.py
│   │   ├── app.py                           # FastAPI application
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── health.py                    # Health check endpoints
│   │       └── summary.py                   # Analysis endpoints
│   │
│   ├── cli/                                 # CLI (Typer)
│   │   ├── __init__.py
│   │   └── app.py                           # CLI commands (find, load, summary, etc.)
│   │
│   ├── visualization/                       # Visualization Layer
│   │   ├── __init__.py
│   │   └── plots.py                         # SWATPlotter with 4 plot types
│   │
│   └── llm/                                 # LLM Integration
│       ├── __init__.py
│       ├── prompts.py                       # Prompt templates
│       └── rag.py                           # RAG system (skeleton)
│
├── docs/
│   ├── architecture.md                      # Architecture overview
│   ├── GETTING_STARTED.md                   # Getting started guide
│   └── DEVELOPMENT.md                       # Development guide
│
├── examples/
│   └── basic_usage.py                       # Python usage examples
│
├── tests/
│   └── unit/
│       └── test_version.py                  # Basic test
│
├── pyproject.toml                           # Project metadata and dependencies
├── README.md                                # Main documentation
├── README_MCP.md                            # MCP server documentation
├── .env.example                             # Environment configuration template
├── .gitignore                               # Git ignore rules
└── PROJECT_SUMMARY.md                       # This file
```

## 🔧 Key Components

### 1. Core Domain Models (`core/projects.py`)

**Classes:**
- `SWATFileType` - Enum of SWAT file types (input/output)
- `SWATFile` - Represents a single SWAT file
- `SWATProject` - Complete project with all files
- `SWATProjectLocator` - Find and scan SWAT projects

**Key Features:**
- File type categorization (input vs output)
- Project validation
- Recursive project discovery
- File metadata extraction

### 2. Data Access Layer (`data_access/`)

**Readers:**
- `SWATFileReader` - Base reader class
- `OutputReader` - Parse SWAT output files (.rch, .sub, .hru)
- `ControlFileReader` - Parse control file (file.cio)
- `SubbasinFileReader` - Parse subbasin files (.sub)
- `HRUFileReader` - Parse HRU files (.hru)

**Schemas:**
- `OutputData` - Base output data structure
- `ReachOutput` - Reach-specific output
- `SubbasinOutput` - Subbasin-specific output
- `HRUOutput` - HRU-specific output
- `WaterBalanceData` - Water balance components

### 3. Services Layer (`services/`)

**ProjectManager:**
- Load/validate projects
- Find projects in directory trees
- Project info and metadata

**SummarizeService:**
- Project summaries
- Output summaries
- File counts and statistics

**AnalysisService:**
- Variable statistics (mean, std, min, max, etc.)
- Time series extraction
- Water balance calculation
- Scenario comparison (skeleton)

### 4. MCP Server (`integrations/mcp/server.py`)

**9 MCP Tools:**
1. `find_swat_projects` - Search for SWAT projects
2. `load_swat_project` - Load a project
3. `get_project_summary` - Get project metadata
4. `get_output_summary` - Summarize outputs
5. `get_variable_statistics` - Calculate stats
6. `get_time_series` - Extract time series
7. `calculate_water_balance` - Water budget
8. `plot_time_series` - Generate time series plot
9. `plot_comparison` - Compare multiple variables

**Resources:**
- `swat://project/{name}` - Project data
- `swat://output/{type}` - Output data

### 5. Visualization (`visualization/plots.py`)

**SWATPlotter Methods:**
- `plot_time_series()` - Time series visualization
- `plot_comparison()` - Multi-variable comparison
- `plot_distribution()` - Histogram
- `plot_scatter()` - Scatter plot

All plots return base64-encoded PNG images.

### 6. CLI (`cli/app.py`)

**Commands:**
- `swat-copilot find` - Find projects
- `swat-copilot load` - Load a project
- `swat-copilot summary` - Project summary
- `swat-copilot outputs` - Output summary
- `swat-copilot stats` - Variable statistics
- `swat-copilot serve-mcp` - Start MCP server
- `swat-copilot version` - Show version

### 7. REST API (`api/`)

**Endpoints:**
- `GET /health` - Health check
- `POST /api/v1/projects/load` - Load project
- `GET /api/v1/projects/find` - Find projects
- `GET /api/v1/projects/summary` - Project summary
- `GET /api/v1/projects/outputs/summary` - Output summary
- `GET /api/v1/analysis/variable/statistics` - Variable stats
- `GET /api/v1/analysis/water-balance` - Water balance

## 📦 Dependencies

### Core Dependencies
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `pydantic` - Data validation
- `mcp` - Model Context Protocol

### API & CLI
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `typer` - CLI framework
- `rich` - Terminal formatting

### Visualization
- `matplotlib` - Plotting
- `seaborn` - Statistical visualization

### Optional
- `openai` - OpenAI integration
- `anthropic` - Anthropic Claude integration
- `geopandas` - Geospatial features (future)

## 🚀 Usage Examples

### As MCP Server

```bash
# Start server
python -m swat_copilot.integrations.mcp
```

Configure in Claude Desktop:
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

### As Python Library

```python
from pathlib import Path
from swat_copilot.services.project_manager import ProjectManager
from swat_copilot.services.analysis import AnalysisService

# Load project
manager = ProjectManager()
project = manager.load_project(Path("/path/to/project"))

# Analyze
analyzer = AnalysisService(project)
stats = analyzer.get_variable_statistics("FLOW_OUT", "reach")
print(f"Mean streamflow: {stats['mean']:.2f} m³/s")
```

### As CLI

```bash
# Find projects
swat-copilot find /models

# Load and analyze
swat-copilot load /models/my_watershed
swat-copilot stats FLOW_OUT --output-type reach
```

### As REST API

```bash
# Start server
uvicorn swat_copilot.api.app:app --reload

# Access at http://localhost:8000/docs
```

## 🎨 Architecture Principles

1. **Layered Architecture**: Clear separation between domain, data access, services, and interfaces
2. **Dependency Direction**: Lower layers don't depend on higher layers
3. **Type Safety**: Full type hints throughout
4. **Testability**: Services are easily mockable
5. **Extensibility**: Easy to add new file readers, tools, or endpoints

## 🔍 SWAT File Types Supported

### Input Files
- Master Watershed (`.Master.Watershed.dat`)
- Control File (`file.cio`)
- Subbasin files (`.sub`)
- HRU files (`.hru`)
- Routing files (`.rte`)
- Weather files (`.pcp`, `.tmp`, `.slr`, `.hmd`, `.wnd`)
- Soil files (`.sol`)
- Management files (`.mgt`)
- Groundwater files (`.gw`)
- Reservoir files (`.res`)
- Pond files (`.pnd`)

### Output Files
- Reach outputs (`output.rch`)
- Subbasin outputs (`output.sub`)
- HRU outputs (`output.hru`)
- Reservoir outputs (`output.rsv`)
- Standard output (`output.std`)

## 🧪 Common SWAT Variables

### Reach Variables
- `FLOW_OUT` - Streamflow (m³/s)
- `SED_OUT` - Sediment (metric tons)
- `ORGN_OUT` - Organic nitrogen (kg N)
- `ORGP_OUT` - Organic phosphorus (kg P)
- `NO3_OUT` - Nitrate (kg N)
- `SOLP_OUT` - Soluble phosphorus (kg P)

### Subbasin Variables
- `PRECIP` - Precipitation (mm)
- `SURQ` - Surface runoff (mm)
- `LATQ` - Lateral flow (mm)
- `GW_Q` - Groundwater flow (mm)
- `ET` - Evapotranspiration (mm)
- `PET` - Potential ET (mm)

## 📝 Next Steps

### Ready to Implement
The skeleton is complete and ready for:
1. Adding actual SWAT projects for testing
2. Implementing real file parsers (currently simplified)
3. Adding more analysis functions
4. Creating comprehensive tests
5. Adding calibration tools
6. Implementing RAG with SWAT documentation

### Future Enhancements
- [ ] SWAT+ support
- [ ] Geospatial visualization
- [ ] Parameter sensitivity analysis
- [ ] Multi-scenario comparison
- [ ] Automated calibration
- [ ] Database persistence
- [ ] Web dashboard
- [ ] Documentation generation

## 🛠️ Development Workflow

1. **Install**: `pip install -e ".[dev]"`
2. **Format**: `black src/ tests/`
3. **Lint**: `ruff check src/`
4. **Type Check**: `mypy src/`
5. **Test**: `pytest --cov`
6. **Run MCP**: `swat-copilot serve-mcp`

## 📚 Documentation

- [README.md](README.md) - Main documentation
- [README_MCP.md](README_MCP.md) - MCP server guide
- [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) - Installation and basics
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guide
- [docs/architecture.md](docs/architecture.md) - Architecture overview

## 🎓 Learning Resources

- **SWAT Model**: https://swat.tamu.edu/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Typer**: https://typer.tiangolo.com/

## ✅ What's Been Created

This repository now includes:

✅ Complete layered architecture
✅ MCP server with 9 tools
✅ REST API with FastAPI
✅ CLI with Typer
✅ Visualization system
✅ Configuration management
✅ File readers (skeleton)
✅ Analysis services
✅ LLM integration helpers
✅ Comprehensive documentation
✅ Example code
✅ Development guides
✅ Type hints throughout
✅ Proper package structure

## 🎉 Ready to Use

The framework is **complete and ready** for:
- Testing with real SWAT projects
- Adding specific parsers for your SWAT version
- Extending with custom analysis functions
- Integration with AI assistants via MCP
- Building custom tools on top of the API

Just add your SWAT project data and start using!
