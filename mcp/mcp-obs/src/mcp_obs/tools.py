"""Tool schemas, handlers, and registry for the observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.client import ObservabilityClient


class LogsSearchQuery(BaseModel):
    """Query for searching logs."""

    query: str = Field(
        description="LogsQL query (e.g., 'service.name:\"Learning Management Service\" severity:ERROR')"
    )
    limit: int = Field(default=100, ge=1, le=1000, description="Max log entries to return")
    time_range: str = Field(default="1h", description="Time range (e.g., '1h', '10m', '1d')")


class LogsErrorCountQuery(BaseModel):
    """Query for counting errors."""

    service: str | None = Field(default=None, description="Optional service name to filter by")
    time_range: str = Field(default="1h", description="Time range (e.g., '1h', '10m', '1d')")


class TracesListQuery(BaseModel):
    """Query for listing traces."""

    service: str | None = Field(default=None, description="Optional service name to filter by")
    limit: int = Field(default=20, ge=1, le=100, description="Max traces to return")


class TracesGetQuery(BaseModel):
    """Query for fetching a specific trace."""

    trace_id: str = Field(description="The trace ID to fetch")


ToolPayload = BaseModel | Sequence[BaseModel] | dict
ToolHandler = Callable[[ObservabilityClient, BaseModel], Awaitable[ToolPayload]]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    """Specification for an MCP tool."""

    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        """Convert to MCP Tool type."""
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Search logs using LogsQL."""
    if not isinstance(args, LogsSearchQuery):
        raise TypeError(f"Expected LogsSearchQuery, got {type(args).__name__}")
    return await client.logs_search(args.query, args.limit, args.time_range)


async def _logs_error_count(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Count errors per service."""
    if not isinstance(args, LogsErrorCountQuery):
        raise TypeError(f"Expected LogsErrorCountQuery, got {type(args).__name__}")
    return await client.logs_error_count(args.service, args.time_range)


async def _traces_list(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """List recent traces."""
    if not isinstance(args, TracesListQuery):
        raise TypeError(f"Expected TracesListQuery, got {type(args).__name__}")
    return await client.traces_list(args.service, args.limit)


async def _traces_get(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Fetch a specific trace by ID."""
    if not isinstance(args, TracesGetQuery):
        raise TypeError(f"Expected TracesGetQuery, got {type(args).__name__}")
    return await client.traces_get(args.trace_id)


TOOL_SPECS = (
    ToolSpec(
        "logs_search",
        "Search logs in VictoriaLogs using LogsQL. Use for finding specific log entries, errors, or events.",
        LogsSearchQuery,
        _logs_search,
    ),
    ToolSpec(
        "logs_error_count",
        "Count errors per service over a time window. Use to quickly see which services have errors.",
        LogsErrorCountQuery,
        _logs_error_count,
    ),
    ToolSpec(
        "traces_list",
        "List recent traces from VictoriaTraces. Use to find traces for a specific service.",
        TracesListQuery,
        _traces_list,
    ),
    ToolSpec(
        "traces_get",
        "Fetch a specific trace by ID. Use to inspect the full span hierarchy of a request.",
        TracesGetQuery,
        _traces_get,
    ),
)

TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
