"""Client for querying VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import httpx
from typing import Any


class ObservabilityClient:
    """Client for querying VictoriaLogs and VictoriaTraces."""

    def __init__(self, victorialogs_url: str, victoriatraces_url: str) -> None:
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victoriatraces_url = victoriatraces_url.rstrip("/")
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> ObservabilityClient:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    # VictoriaLogs methods

    async def logs_search(
        self, query: str, limit: int = 100, time_range: str = "1h"
    ) -> list[dict[str, Any]]:
        """
        Search logs in VictoriaLogs using LogsQL.

        Args:
            query: LogsQL query string (e.g., 'service.name:"Learning Management Service" severity:ERROR')
            limit: Maximum number of log entries to return
            time_range: Time range for the query (e.g., '1h', '10m', '1d')

        Returns:
            List of log entries as dictionaries
        """
        # Prepend time range if not already in query
        if "_time:" not in query:
            query = f"_time:{time_range} {query}"

        url = f"{self.victorialogs_url}/select/logsql/query"
        params = {"query": query, "limit": limit}

        response = await self._client.get(url, params=params)
        response.raise_for_status()

        # VictoriaLogs returns newline-delimited JSON
        lines = response.text.strip().split("\n")
        results = []
        for line in lines:
            if line.strip():
                results.append(httpx.Response(line.encode()).json() if False else __import__("json").loads(line))
        return results

    async def logs_error_count(
        self, service: str | None = None, time_range: str = "1h"
    ) -> dict[str, int]:
        """
        Count errors per service over a time window.

        Args:
            service: Optional service name to filter by
            time_range: Time range for the query

        Returns:
            Dictionary mapping service names to error counts
        """
        query = f"_time:{time_range} severity:ERROR"
        if service:
            query += f' service.name:"{service}"'

        logs = await self.logs_search(query, limit=1000, time_range=time_range)

        # Count errors by service
        error_counts: dict[str, int] = {}
        for log in logs:
            service_name = log.get("service.name", "unknown")
            error_counts[service_name] = error_counts.get(service_name, 0) + 1

        return error_counts

    # VictoriaTraces methods

    async def traces_list(
        self, service: str | None = None, limit: int = 20
    ) -> list[dict[str, Any]]:
        """
        List recent traces.

        Args:
            service: Optional service name to filter by
            limit: Maximum number of traces to return

        Returns:
            List of trace summaries
        """
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces"
        params = {"limit": limit}
        if service:
            params["service"] = service

        response = await self._client.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        # Jaeger API returns {"data": [...]}
        return data.get("data", [])

    async def traces_get(self, trace_id: str) -> dict[str, Any]:
        """
        Fetch a specific trace by ID.

        Args:
            trace_id: The trace ID to fetch

        Returns:
            Full trace data with spans
        """
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"
        response = await self._client.get(url)
        response.raise_for_status()

        data = response.json()
        # Jaeger API returns {"data": [...]}
        traces = data.get("data", [])
        return traces[0] if traces else {}
