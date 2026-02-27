# Personal Assistant (Strands Multi-Agent)

This project implements a personal assistant using the Strands "agent-as-tool" pattern.  
One orchestrator agent routes requests to specialized sub-agents for calendar management, coding, and web research.

## Architecture
![architecture](images/multi-agent-architecture.png)

## What It Can Do

### Personal Assistant Orchestrator
- Receives user prompts and delegates to the right sub-agent(s).
- Handles both single-domain and multi-domain requests in one conversation.

### Calendar Assistant (`agents/calendar_assistant.py`)
- Create appointments (`YYYY-MM-DD HH:MM` format)
- List all appointments
- Update appointments by `appointment_id`
- Get agenda for a specific date (`YYYY-MM-DD`)
- Uses local SQLite storage: `appointments.db`

### Code Assistant (`agents/code_assistant.py`)
- Python REPL execution
- Multi-file editing with editor tool
- Shell command execution
- Journal support for notes/work tracking

### Search Assistant (`agents/search_assistant.py`)
- Real-time web research via Perplexity MCP
- Source-aware research responses
- Uses Docker to run `mcp/perplexity-ask`

## Project Layout

```text
personal_assistant.py                # Main orchestrator
agents/
  calendar_assistant.py              # Calendar agent tool wrapper
  code_assistant.py                  # Coding agent tool wrapper
  search_assistant.py                # Search agent tool wrapper (MCP + Docker)
calendar_tools/
  create_appointment.py
  list_appointments.py
  update_appointment.py
  get_agenda.py
config/
  env_setup.py                       # Loads .env from repo root
  constants.py                       # SESSION_ID + BEDROCK_MODEL_ID defaults
appointments.db                      # Created at runtime
```

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended dependency manager)
- AWS account with Bedrock model access
- Docker Desktop running (required for search flow)
- Perplexity API key (required for search flow)

## Setup

1. Create and sync environment:

```bash
uv venv
uv sync
```

2. Configure AWS credentials (recommended):

```bash
aws configure
```

3. Create `.env` in repo root:

```dotenv
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0
PERPLEXITY_API_KEY=...
SESSION_ID=personal-assistant-dev
```

Notes:
- `.env` is auto-loaded by all assistant entry points in this repo.
- `PERPLEXITY_API_KEY` and Docker are only required when search capabilities are used.

## Run

From repo root:

### Personal Assistant (orchestrator)
```bash
uv run python -u personal_assistant.py
```

### Calendar Assistant only
```bash
uv run python -u -m agents.calendar_assistant
```

### Code Assistant only
```bash
uv run python -u -m agents.code_assistant
```

### Search Assistant only
```bash
uv run python -u -m agents.search_assistant
```

## Example Prompts

### Calendar
- `Create an appointment on 2026-03-05 10:30 at Office titled Team Sync with description Sprint planning`
- `List all appointments`
- `What is my agenda for 2026-03-05?`

### Code
- `Create a Python function to reverse a string`
- `Write a CLI timer script and explain how to run it`

### Search
- `What are the latest AWS Bedrock announcements this month? Include sources.`

### Multi-domain orchestration
- `Schedule a focus session on 2026-03-06 09:00 at Home titled Build Demo with description Work on MVP, then give me a Python starter script for a CLI timer, and finally find one article on productivity techniques with source links.`

## Troubleshooting

- `PERPLEXITY_API_KEY environment variable is required`  
  Add the key in `.env` and restart.

- Search assistant fails to initialize  
  Ensure Docker is running and `docker ps` works.

- Bedrock permission/model access errors  
  Verify AWS credentials and Bedrock model access in your configured region.

- `ModuleNotFoundError` when running assistant files directly  
  Run from repo root using module mode:
  - `uv run python -u -m agents.calendar_assistant`
  - `uv run python -u -m agents.code_assistant`
  - `uv run python -u -m agents.search_assistant`
