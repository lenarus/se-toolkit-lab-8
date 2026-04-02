"""Settings for the observability MCP server."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the observability MCP server."""

    model_config = SettingsConfigDict(env_prefix="NANOBOT_", env_file=".env.docker.secret", extra="ignore")

    victorialogs_url: str = Field(..., alias="NANOBOT_VICTORIALOGS_URL")
    victoriatraces_url: str = Field(..., alias="NANOBOT_VICTORIATRACES_URL")


def resolve_settings() -> Settings:
    """Resolve settings from environment."""
    return Settings()
