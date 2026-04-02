---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use the LMS MCP tools to query live data from the Learning Management System backend.

## Available Tools

| Tool | Description | Requires Lab? |
|------|-------------|---------------|
| `lms_health` | Check if the LMS backend is healthy and report item count | No |
| `lms_labs` | List all labs available in the LMS | No |
| `lms_learners` | List all learners registered in the LMS | No |
| `lms_pass_rates` | Get pass rates (avg score, attempt count per task) for a lab | Yes |
| `lms_timeline` | Get submission timeline (date + count) for a lab | Yes |
| `lms_groups` | Get group performance (avg score + student count) for a lab | Yes |
| `lms_top_learners` | Get top learners by average score for a lab | Yes |
| `lms_completion_rate` | Get completion rate (passed / total) for a lab | Yes |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline to fetch latest data | No |

## Strategy

### When the user asks about scores, pass rates, completion, groups, timeline, or top learners without naming a lab:

1. First call `lms_labs` to get the list of available labs
2. If multiple labs exist, use the `structured-ui` skill to present a choice to the user
3. Use each lab's `title` field as the user-facing label
4. Pass the lab identifier (e.g., `lab-01`) to the specific tool once the user chooses

### When the user asks for a specific lab by name or ID:

- Call the appropriate tool directly with the lab parameter
- Example: "Show me scores for lab-03" → call `lms_pass_rates({"lab": "lab-03"})`

### Formatting responses:

- Format percentages with one decimal place (e.g., `89.1%`)
- Format counts with commas for readability (e.g., `1,234`)
- Keep responses concise — lead with the answer, then show details if relevant
- When showing multiple labs, use a table format

### When the user asks "what can you do?":

Explain your current capabilities clearly:
- You can query live LMS data using MCP tools
- You can check backend health, list labs and learners
- You can get analytics: pass rates, completion rates, timelines, group performance, top learners
- You can trigger the sync pipeline to fetch fresh data from the autochecker
- You don't have access to modify data — only read and analyze

## Examples

**User:** "Show me the scores"
**You:** Call `lms_labs` first, then present choices via structured UI

**User:** "What labs are available?"
**You:** Call `lms_labs` and list them with titles

**User:** "Is the backend healthy?"
**You:** Call `lms_health` and report status + item count

**User:** "Which lab has the lowest pass rate?"
**You:** Call `lms_labs`, then call `lms_completion_rate` for each lab, compare and report

**User:** "Show me the top 3 learners in lab-02"
**You:** Call `lms_top_learners({"lab": "lab-02", "limit": 3})`
