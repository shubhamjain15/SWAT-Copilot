# Architecture Overview

The repository is organised around clear layering to keep concerns isolated:

- **config** – loading runtime configuration and environment overrides.
- **core** – domain models that understand the layout and semantics of SWAT projects.
- **data_access** – readers and serializers that communicate with files and external stores.
- **services** – orchestration logic that coordinates domain objects to answer questions.
- **api / cli** – delivery mechanisms (FastAPI and Typer) that expose functionality to users.
- **visualization** – Matplotlib-based helpers for charts and figures.
- **llm** – prompt templates and retrieval helpers for language model integrations.
- **integrations** – placeholders for external protocol support such as MCP.

This structure allows each layer to evolve independently while keeping the codebase discoverable for SWAT-Copilot contributors.
