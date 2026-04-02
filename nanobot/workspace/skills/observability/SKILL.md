---
name: observability
description: Use observability tools to investigate logs and traces
always: true
---

# Observability Skill

Use the observability MCP tools to investigate logs and traces when diagnosing issues.

## Available Tools

| Tool | Description | When to Use |
|------|-------------|-------------|
| `logs_search` | Search logs in VictoriaLogs using LogsQL | Find specific log entries, errors, or events |
| `logs_error_count` | Count errors per service over a time window | Quick overview of which services have errors |
| `traces_list` | List recent traces from VictoriaTraces | Find traces for a specific service |
| `traces_get` | Fetch a specific trace by ID | Inspect full span hierarchy of a request |

## Strategy

### When the user asks about errors or issues:

1. **Start with `logs_error_count`** to quickly see which services have errors in the relevant time window
2. **Use `logs_search`** to inspect the specific error messages and extract details like `trace_id`
3. **If you find a `trace_id` in the logs**, call `traces_get` to fetch the full trace and understand the request flow
4. **Summarize findings concisely** — don't dump raw JSON

### When the user asks "What went wrong?" or "Check system health":

Guide the agent through a **one-shot investigation** that chains log and trace tools:

1. **`logs_error_count`** on a fresh recent window (e.g., last 5-10 minutes)
2. **`logs_search`** scoped to the most likely failing service (e.g., "Learning Management Service")
3. **`traces_get`** for the most relevant recent `trace_id` from the error logs
4. **One short explanation** that explicitly mentions both **log evidence** and **trace evidence**

The goal is a single coherent investigation that:
- Names the affected service
- Identifies the root failing operation (e.g., database query, external API call)
- Cites specific log messages and trace span errors
- Explains what went wrong in plain language

### Query patterns for VictoriaLogs (LogsQL):

- Filter by service: `service.name:"Learning Management Service"`
- Filter by severity: `severity:ERROR` or `severity:WARNING`
- Filter by event: `event:"db_query"`
- Filter by time: `_time:10m` (last 10 minutes), `_time:1h` (last hour)
- Combine filters: `_time:10m service.name:"Learning Management Service" severity:ERROR`

### Query patterns for VictoriaTraces:

- List traces for a service: use `traces_list` with `service` parameter
- Get a specific trace: use `traces_get` with the `trace_id` from logs

## Response Format

- **Lead with the answer**: "Yes, there are errors" or "No errors found"
- **Summarize, don't dump**: Extract key information from logs/traces, don't show raw JSON
- **Include trace IDs when relevant**: If you found a trace ID, mention it so the user can look it up
- **Use time context**: Always mention the time window you searched (e.g., "in the last 10 minutes")
- **Chain evidence**: When investigating failures, cite both log evidence and trace evidence

## Examples

**User:** "Any errors in the last hour?"
**You:** Call `logs_error_count({"time_range": "1h"})` first, then summarize

**User:** "Any LMS backend errors in the last 10 minutes?"
**You:** Call `logs_error_count({"service": "Learning Management Service", "time_range": "10m"})`

**User:** "What went wrong?" or "Check system health"
**You:**
1. Call `logs_error_count({"time_range": "5m"})` to see which services have recent errors
2. Call `logs_search({"query": "service.name:\"Learning Management Service\" severity:ERROR _time:5m", "limit": 10})`
3. Extract `trace_id` from the most recent error log
4. Call `traces_get({"trace_id": "..."})` to fetch the full trace
5. Summarize: "The LMS backend failed when querying PostgreSQL. Logs show 'connection is closed' error during db_query. Trace [trace_id] confirms the failure originated in the items router, which returned 404 instead of the actual database error."

**User:** "Show me recent traces for the backend"
**You:** Call `traces_list({"service": "Learning Management Service", "limit": 10})`
