# Haircut Booking Agent

A conversational AI agent that books same-day haircut appointments end-to-end — checks availability, collects customer details, and confirms the booking — built with **LangGraph**, **Claude (Anthropic)**, **FastAPI**, and **React**.

## What it does

A customer opens the chat widget and talks to the agent like they would a receptionist:

- The agent asks for a preferred time, service type, name, and phone number — a couple of questions at a time, not a form dump.
- It checks real-time availability against a small booking store before confirming any slot, and offers alternatives if the requested time is taken.
- Once every detail is confirmed, it finalizes the booking and the conversation is marked done.
- Conversations are resumable: each chat session is tracked by a `thread_id`, so a user can leave and come back mid-booking without losing context.

## Architecture

The agent is modeled as an explicit **state graph** (LangGraph) rather than a single prompt-and-pray loop, which keeps the control flow (when to call a tool vs. ask the user vs. end the conversation) deterministic and easy to reason about:

```
prepare_input ──▶ llm ──┬──▶ tool ──▶ parse_tool_output ──▶ llm
                         ├──▶ human_input ──▶ llm
                         └──▶ END (booking confirmed)
```

- **`llm` node** — Claude (`claude-sonnet-4-6` via `langchain-anthropic`) decides whether to respond, call a tool, or ask the customer something.
- **`tool` node** — executes whichever tool Claude called.
- **`human_input` node** — uses LangGraph's `interrupt()` to pause the graph and wait for the next user message, which is what makes the API's `/start` + `/resume` request/response shape work cleanly for a chat UI.
- **`parse_tool_output` node** — lifts booking details out of tool results and into graph state once `finish_booking` succeeds.
- State is checkpointed in-memory per `thread_id` (`MemorySaver`), so a conversation can be resumed across HTTP requests.

### Tools

| Tool | Purpose |
|---|---|
| `find_availability(time)` | Looks up whether a requested time slot is open; returns alternatives if not. |
| `finish_booking(time, service_type, customer_name, phone)` | Finalizes the appointment and persists it. |

Bookings/availability are persisted to a flat JSON file (`database/bookings.json`) — intentionally simple, since the focus of this project is the agent's conversational and control-flow design rather than the data layer.

## Tech stack

- **Agent orchestration:** LangGraph (state graph, interrupts, checkpointing)
- **LLM:** Anthropic Claude via `langchain-anthropic`
- **Backend:** FastAPI (async endpoints, Pydantic schemas)
- **Frontend:** React + Vite — a minimal chat UI that talks to the API over `/start` and `/resume`

## Project structure

```
agent/          LangGraph state machine: nodes, state schema, system prompt
api/            FastAPI app and routers (/start, /resume)
core/           Pydantic request/response schemas, settings/env loading
database/       JSON-backed booking store + helpers
tools/          LangChain tools the agent can call (availability, booking)
agent_ui/       React + Vite chat frontend
examples/       Standalone script to run the agent from the terminal
```

## Running it locally

**Backend**

```bash
python -m venv env && source env/bin/activate
pip install -r requirements.txt

# create a .env with:
# ANTHROPIC_API_KEY=your-key-here

uvicorn api.main:app --reload
```

**Frontend**

```bash
cd agent_ui
npm install
npm run dev
```

**API quickstart**

```bash
curl -X POST localhost:8000/start -H "x-user-id: demo"
curl -X POST localhost:8000/resume \
  -H "x-user-id: demo" -H "Content-Type: application/json" \
  -d '{"thread_id": "<thread_id from /start>", "message": "2pm for a fade"}'
```

## Notes

This project only books appointments for the current day by design — it's a focused demo of agentic conversation + tool-use control flow, not a production scheduling system.
