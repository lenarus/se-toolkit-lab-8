# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->

**Question 1: "What is the agentic loop?"**

The **agentic loop** is the core reasoning cycle that autonomous AI agents use to accomplish tasks. It's a continuous feedback loop with these key phases:

| Phase     | Description                                                           |
|-----------|-----------------------------------------------------------------------|
| Perceive  | Take in information (user requests, tool outputs, environment state)  |
| Reason    | Analyze, plan, and decide on the next action                          |
| Act       | Execute actions using available tools                                 |
| Observe   | Evaluate the results of those actions                                 |
| Iterate   | Repeat until the goal is reached or blocked                           |

Why It Matters

This loop enables agents to:

- Decompose complex problems into sequential steps
- Adapt dynamically based on real-world feedback
- Self-correct when actions produce unexpected results
- Use tools autonomously without step-by-step human guidance

Example (My Workflow)

When you ask me to do something:

1. I perceive your request
2. I reason about what tools/files I need
3. I act by calling tools (read_file, exec, web_search, etc.)
4. I observe the tool outputs
5. I iterate until I have a complete answer

This is what distinguishes an agent from a simple Q&A model—the ability to take multiple autonomous steps toward a goal.

**Question 2: "What labs are available in our LMS?"**

Based on my exploration of the LMS in this SE Toolkit Lab environment, here are the available labs:

**Required Labs**

| Lab     | Topic                                                                 |
|---------|-----------------------------------------------------------------------|
| Task 1  | Set Up the Agent — Install nanobot, connect to LMS backend via MCP, write skill prompts |
| Task 2  | Deploy the Agent — Docker deployment, WebSocket channel, Flutter web client |
| Task 3  | Observability — VictoriaLogs, VictoriaTraces, MCP tools for logs/traces |
| Task 4  | Failure Diagnosis — Investigate failures, proactive health checks, bug fix |

**Optional Labs**

| Lab              | Topic                                                        |
|------------------|--------------------------------------------------------------|
| Optional Task 1  | Telegram Bot Client — Add a Telegram bot as an additional chat channel |

These labs are stored in the repository at:

- Required: /lab/tasks/required/task-1.md through task-4.md
- Optional: /lab/tasks/optional/task-1.md

The LMS backend also tracks learner data (scores, pass rates, completion status) for these labs. Once you have the nanobot agent connected to the LMS via MCP tools (covered in Task 1), you can query live data like:

- "What labs are available?"
- "Show me pass rates for each lab"
- "Which learners completed Task 3?"

---

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

**Question 1: "What labs are available?"**

Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Is there a specific lab you'd like to explore or get more information about?

**Question 2: "Is the LMS backend healthy?"**

Yes, the LMS backend is healthy! ✅

- Status: healthy
- Item count: 56
- Errors: none

**Complex question: "Which lab has the lowest pass rate?"**

Based on the completion rates:

| Lab     | Completion Rate | Passed | Total |
|---------|-----------------|--------|-------|
| Lab 01  | 100.0%          | 258    | 258   |
| Lab 02  | 89.1%           | 131    | 147   |
| Lab 03  | 89.1%           | 156    | 175   |
| Lab 04  | 96.7%           | 238    | 246   |
| Lab 05  | 98.4%           | 246    | 250   |
| Lab 06  | 98.4%           | 242    | 246   |
| Lab 07  | 99.6%           | 236    | 237   |
| Lab 08  | 0.0%            | 0      | 0     |

Lab 02 and Lab 03 are tied for the lowest pass rate at 89.1% among labs with actual submissions.

Note: Lab 08 shows 0.0% because it has no submissions yet (0 passed out of 0 total), so it's not a meaningful comparison.

---

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

**Question: "Show me the scores" (without specifying a lab)**

I'll check what labs are available in the LMS first.

There are 8 labs available. Which lab would you like to see the scores for?

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 – Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Please let me know which lab you'd like to see, or if you'd like to see scores for all labs.

---

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
