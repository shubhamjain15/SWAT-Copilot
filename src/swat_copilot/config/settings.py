"""Runtime configuration and environment settings."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "SWAT-Copilot"
    debug: bool = False
    log_level: str = "INFO"

    # SWAT Project Defaults
    default_swat_project_path: Optional[Path] = None
    swat_project_extensions: list[str] = Field(
        default_factory=lambda: [".txt", ".dat", ".sub", ".rte", ".hru", ".output"]
    )

    # LLM Configuration
    llm_provider: str = "openai"
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # MCP Server Configuration
    mcp_server_name: str = "swat-copilot"
    mcp_server_version: str = "0.0.1"
    mcp_transport: str = "stdio"  # stdio or http

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False

    # Visualization
    plot_style: str = "seaborn-v0_8"
    plot_dpi: int = 100
    plot_figsize: tuple[int, int] = (10, 6)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
