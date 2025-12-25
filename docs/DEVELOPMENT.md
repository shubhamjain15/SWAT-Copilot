# Development Guide

This guide covers development workflows, architecture decisions, and how to extend SWAT-Copilot.

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Steps

```bash
# Clone repository
git clone <repository-url>
cd SWAT-Copilot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Architecture Overview

SWAT-Copilot follows a **layered architecture** to maintain separation of concerns:

### Layer 1: Configuration (`config/`)
- **Purpose**: Application settings and environment configuration
- **Key Files**: `settings.py`
- **Dependencies**: Pydantic for validation

### Layer 2: Core Domain (`core/`)
- **Purpose**: Business entities and domain logic
- **Key Files**: `projects.py` (SWATProject, SWATFile, SWATProjectLocator)
- **Dependencies**: Python standard library only

### Layer 3: Data Access (`data_access/`)
- **Purpose**: File I/O, parsing, and data serialization
- **Key Files**: `readers.py`, `schemas.py`
- **Dependencies**: pandas for data handling

### Layer 4: Services (`services/`)
- **Purpose**: Orchestration and business operations
- **Key Files**:
  - `project_manager.py` - Project lifecycle management
  - `summary.py` - Summary generation
  - `analysis.py` - Data analysis operations
- **Dependencies**: Core, data access layers

### Layer 5: Integrations (`integrations/`, `api/`, `cli/`)
- **Purpose**: External interfaces and protocols
- **Components**:
  - `integrations/mcp/` - MCP server
  - `api/` - REST API (FastAPI)
  - `cli/` - Command-line interface (Typer)
- **Dependencies**: All lower layers

### Support Layers
- **Visualization** (`visualization/`) - Matplotlib-based plotting
- **LLM** (`llm/`) - Prompts and RAG for AI integration

## Code Style and Standards

### Python Style

We follow PEP 8 with these tools:

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

### Code Quality Rules

1. **Type Hints**: All functions must have type hints
2. **Docstrings**: All public functions/classes need docstrings
3. **Line Length**: 100 characters max
4. **Imports**: Sorted with `ruff` (isort rules)

Example:
```python
def analyze_variable(
    variable: str,
    output_type: str = "reach",
) -> dict[str, float]:
    """
    Analyze a SWAT variable.

    Args:
        variable: Variable name
        output_type: Type of output

    Returns:
        Dictionary with statistics
    """
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=swat_copilot --cov-report=html

# Specific test file
pytest tests/unit/test_projects.py

# Specific test
pytest tests/unit/test_projects.py::test_swat_project_creation
```

### Writing Tests

Place tests in `tests/`:
- `tests/unit/` - Unit tests (fast, isolated)
- `tests/integration/` - Integration tests (slower, multi-component)

Example test:
```python
"""Unit tests for project manager."""
import pytest
from pathlib import Path
from swat_copilot.services.project_manager import ProjectManager


def test_project_manager_initialization():
    """Test ProjectManager can be initialized."""
    manager = ProjectManager()
    assert manager is not None
    assert manager.current_project is None


def test_load_project_invalid_path(tmp_path):
    """Test loading project with invalid path raises error."""
    manager = ProjectManager()
    invalid_path = tmp_path / "nonexistent"

    with pytest.raises(ValueError):
        manager.load_project(invalid_path)
```

## Adding New Features

### Adding a New MCP Tool

1. **Define the tool** in `integrations/mcp/server.py`:

```python
@self.server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools ...
        Tool(
            name="my_new_tool",
            description="Does something useful",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "First parameter",
                    },
                },
                "required": ["param1"],
            },
        ),
    ]
```

2. **Implement the handler**:

```python
@self.server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "my_new_tool":
        return await self._my_new_tool(arguments)
    # ... existing handlers ...

async def _my_new_tool(self, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle my_new_tool execution."""
    result = do_something(arguments["param1"])
    return [TextContent(type="text", text=str(result))]
```

3. **Add service logic** (if needed) in appropriate service class

4. **Write tests**:

```python
async def test_my_new_tool():
    """Test my_new_tool."""
    server = SWATMCPServer()
    result = await server._my_new_tool({"param1": "test"})
    assert len(result) == 1
    assert result[0].type == "text"
```

### Adding a New Service

1. Create file in `services/`:

```python
"""My new service module."""
from swat_copilot.core.projects import SWATProject


class MyService:
    """Service for doing X."""

    def __init__(self, project: SWATProject) -> None:
        """Initialize service."""
        self.project = project

    def do_something(self) -> dict[str, any]:
        """Do something useful."""
        return {"result": "data"}
```

2. Update `services/__init__.py`:

```python
from swat_copilot.services.my_service import MyService

__all__ = ["MyService", ...]
```

3. Write tests in `tests/unit/test_my_service.py`

### Adding New Output Readers

1. Add reader class to `data_access/readers.py`:

```python
class MyFileReader(SWATFileReader):
    """Reader for custom SWAT file format."""

    def read(self) -> dict[str, Any]:
        """Parse the file."""
        lines = self.read_lines()
        # Parse logic here
        return parsed_data
```

2. Add schema to `data_access/schemas.py` if needed

3. Update `core/projects.py` to recognize the file type

## API Development

### Adding API Endpoints

Add routes to `api/routers/`:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/my-endpoint")
async def my_endpoint(param: str) -> dict[str, str]:
    """My API endpoint."""
    return {"result": f"Processed {param}"}
```

Include in `api/app.py`:

```python
from swat_copilot.api.routers import my_router

app.include_router(my_router.router, prefix="/api/v1", tags=["my-feature"])
```

## CLI Development

### Adding CLI Commands

Add commands to `cli/app.py`:

```python
@app.command()
def my_command(
    arg: str = typer.Argument(..., help="An argument"),
    option: bool = typer.Option(False, help="An option"),
) -> None:
    """My CLI command."""
    console.print(f"Processing {arg}")
    if option:
        console.print("Option enabled")
```

## Visualization

### Adding New Plot Types

Add methods to `visualization/plots.py`:

```python
def plot_my_visualization(
    self,
    data: pd.DataFrame,
    title: Optional[str] = None,
) -> str:
    """Create my custom visualization."""
    fig, ax = plt.subplots(figsize=self.settings.plot_figsize)

    # Plotting logic
    ax.plot(data)
    ax.set_title(title or "My Plot")

    return self._figure_to_base64(fig)
```

## Database and State Management

Currently, SWAT-Copilot is **stateless** - each operation loads fresh data. For production use with persistence:

1. Add SQLAlchemy models in `data_access/models.py`
2. Create database service in `services/database.py`
3. Add migrations with Alembic

## Performance Optimization

### Caching

For expensive operations, add caching:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(project_path: str) -> dict[str, Any]:
    """Cached expensive operation."""
    # ... computation ...
    return result
```

### Async Operations

For I/O-bound operations:

```python
import asyncio
from pathlib import Path

async def load_multiple_projects(
    paths: list[Path]
) -> list[SWATProject]:
    """Load multiple projects concurrently."""
    tasks = [load_project_async(p) for p in paths]
    return await asyncio.gather(*tasks)
```

## Documentation

### Code Documentation

Use NumPy-style docstrings:

```python
def my_function(param1: str, param2: int = 0) -> dict[str, Any]:
    """
    Short description.

    Longer description if needed. Can span multiple lines
    and include details about the function's behavior.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)

    Returns:
        Dictionary containing the results

    Raises:
        ValueError: If param1 is empty
        RuntimeError: If processing fails

    Examples:
        >>> result = my_function("test", 5)
        >>> print(result["value"])
        5
    """
    pass
```

### Documentation Generation

```bash
# Generate API docs (future)
mkdocs build
mkdocs serve
```

## Debugging

### Enable Debug Logging

In `.env`:
```
DEBUG=true
LOG_LEVEL=DEBUG
```

In code:
```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug information")
logger.info("Processing file: %s", file_path)
```

### Debugging MCP Server

Add logging to see MCP messages:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Debugging API

Use FastAPI debug mode:
```bash
uvicorn swat_copilot.api.app:app --reload --log-level debug
```

## Release Process

1. Update version in `pyproject.toml` and `src/swat_copilot/__init__.py`
2. Update `CHANGELOG.md`
3. Run full test suite: `pytest`
4. Build distribution: `python -m build`
5. Tag release: `git tag v0.1.0`
6. Push tag: `git push origin v0.1.0`

## Common Issues

### Import Errors
- Ensure package is installed in editable mode: `pip install -e .`
- Check Python path includes src directory

### Type Checking Failures
- Run `mypy src/` to see all type errors
- Add `# type: ignore` only as last resort

### Test Failures
- Ensure test data is available
- Check for hardcoded paths
- Use fixtures for setup/teardown

## Best Practices

1. **Keep layers separate** - Don't import from higher layers into lower layers
2. **Write tests first** - TDD helps design better interfaces
3. **Document as you go** - Easier than documenting later
4. **Small PRs** - Easier to review and merge
5. **Use type hints** - Catches errors early
6. **Handle errors gracefully** - Don't let exceptions crash the server
7. **Log appropriately** - Debug for development, Info for production

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [SWAT Documentation](https://swat.tamu.edu/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)

## Getting Help

- Check existing issues on GitHub
- Review documentation in `docs/`
- Look at example code in `examples/`
- Ask in discussions (if enabled)
