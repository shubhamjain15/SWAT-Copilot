# SWAT-Copilot

LLM-assisted exploration, QA, and visualization for SWAT projects.

## Project Status

This repository is an **active and ongoing effort**. Features and APIs are under continuous development — expect breaking changes until the first stable release.

## Repository Layout

```
SWAT-Copilot/
├── docs/                  # Architecture notes, ADRs, and design references
├── notebooks/
│   └── exploratory/       # Jupyter notebooks for experiments and demos
├── src/
│   └── swat_copilot/
│       ├── api/           # FastAPI application and routers
│       ├── cli/           # Typer-based command line application
│       ├── config/        # Runtime configuration objects
│       ├── core/          # Domain models (SWAT projects, datasets, etc.)
│       ├── data_access/   # Low-level readers and schemas
│       ├── integrations/  # External integration stubs (MCP, etc.)
│       ├── llm/           # Prompt templates and retrieval helpers
│       ├── services/      # Orchestration logic for higher-level tasks
│       └── visualization/ # Plotting helpers and report assets
├── tests/
│   └── unit/              # Automated unit test suites
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
```

This layered structure separates the domain logic (`core`), data access primitives (`data_access`), and orchestration services (`services`). API and CLI entry points sit on top of those layers, with visualization and LLM helpers providing supporting capabilities.

## Quickstart

- Clone this repository locally.
- Open the folder in **VS Code**.
- Use the **Dev Containers** extension → *Reopen in Container*.
- Once the container is built, you’ll have Python, Jupyter, and geospatial libraries pre-installed and ready.

## Contributing

Contributions are welcome! To propose a change:

1. Fork the repository.
2. Create a feature branch from `dev`:
   ```bash
   git checkout dev
   git checkout -b feature/<short-feature-name>
   ```
3. Commit your changes and open a pull request.
