**Product Requirements Document (PRD)**\
**Project:** Agentic AI Business Intelligence Platform\
**Prepared by:** Kevin McCartney with assistance from Project Lead AI\
**Date:** June 13, 2025

---

## 1. Project Overview

**Name:** Agentic AI Business Intelligence Platform\
**One-liner pitch:** Using agentic AI workflows, our app strives to better pinpoint what the data is telling us about your specific business problem, reorganizing it into entities and metadata that can better serve your business needs.

**Problem Statement:**
Modern businesses often face a disconnect between raw data and actionable insight. Traditional BI tools rely heavily on technical expertise, static reports, and predefined models. Our platform leverages agentic AI and orchestrated workflows to help users extract, restructure, and contextualize their data for better outcomes.

---

## 2. Goals & Objectives

**Primary Goal:**\
Enable businesses to structure their data to support efficient, goal-driven problem solving.

**Secondary Goals:**

- Provide agent-guided coaching through workflows
- Visualize structured outputs (reports, summaries, charts)
- Facilitate data upload and interactive refinement

**Definition of Success:**\
A working web app that:

- Connects to and orchestrates n8n agentic workflows
- Supports chat-based user interaction
- Delivers business intelligence outputs from uploaded data

---

## 3. Target Users

**Personas:**

- Consultants
- Project Managers
- Business Analysts
- Solution Architects

**User Technical Level:** Intermediate (familiarity with data concepts, but not programming)

**Access Method:** Web app with user authentication

---

## 4. Core Features

**User-Initiated Workflows:**

- Describe a business problem
- Upload supporting documents (CSV, PDF, TXT)
- Interact via chat interface to refine scope
- Approve inception summary
- Receive structured insight document (PDF/.docx/Chart)

**Data Types Accepted:**

- CSV
- PDF
- TXT
- JSON (future goal)

**Expected Outputs:**

- BI report (PDF, .docx)
- Summarized insights
- Highlighted decisions
- Metadata catalogs
- Conceptual data models

---

## 5. Agentic AI Workflows (via n8n)

### Coordinator Agent Functionality

The Inception Agent Coordinator plays a central role in directing the user's journey through various workflows and agent interactions. This agent is responsible for:

- **Session Initialization:** Initiating context-aware sessions, managing session memory, and collecting relevant user context (persona, intent, uploaded files).
- **Workflow Selection and Dispatch:** Interpreting the user's intent from chat input and routing the request to the appropriate conceptual or physical workflow.
- **Stateful Management:** Tracking which stage the user is in across a multi-step workflow and providing instructions or feedback loops.
- **Feedback Loop Activation:** Handling summary approvals or "need more detail" requests by routing to sub-agents or reengaging clarification prompts.
- **Workflow Monitoring:** Logging agent workflow activity for debugging and optimization, and optionally alerting or escalating stuck sessions.
- **Tool Awareness:** Keeping track of available tools (e.g., PDF parser, vector memory, glossary generator) and choosing which to invoke depending on workflow requirements.
- **Agent Chaining:** Sequencing multiple agents together in longer pipelines and passing refined context between them.

Future enhancements will include protocol compliance for Model Context Protocol (MCP), modular fallback logic, and routing intelligence for workflows of differing complexity and structure.

**Existing Agents:**

- Inception Agent Coordinator
- Domain-specific SME Conversational Agents
- Problem Inception Agent
- Metadata Structuring Agent
- Physical Data Workflow Agents (e.g. Data Dictionary, Schema Attribution)

**System Messages:** Each workflow has a defined role, implemented via system prompts.

**Triggering Method:** Likely via webhook initiated from web app. Other options like polling or message queue under exploration.

---

## 6. User Journey Example

**Example Flow:**

1. User logs in
2. Uploads CSV
3. Enters business challenge in chat
4. Coaching Agent clarifies and refines prompt
5. Inception Agent generates structured summary
6. User reviews and approves
7. Metadata Agent structures glossary/entities
8. Output delivered: business model, glossary, key decisions

**UI Considerations:**

- Persona selector dropdown
- Chat interface for coaching
- Upload panel (CSV/PDF)
- Output panel with export options

---

## 7. Technical Requirements

**Frontend:** React (preferred), others open if suggested by Cursor
**Backend:** Node.js and Flask (compatible with uvicorn and n8n)
**Hosting:** Docker-based containerization with GCP
**Authentication:** Not yet implemented (OAuth planned)
**Dev Tools:** Vite, npm, uvicorn, LiteLLM

---

## 8. API & Workflow Integrations

**External APIs:**

- OpenAI (chat, embeddings)
- Pinecone (vector store)
- n8n (workflow orchestration)

**Tooling Integrations:**

- DataHub (planned for metadata catalog)
- dbt / VaultSpeed / Snowflake (future integrations)

**Note:** Workflow integrations will evolve as MCP architecture is evaluated

---

## 9. Success Metrics

**Short-term:**

- Ability to complete an end-to-end conceptual workflow by next week

**Mid-term:**

- Execute physical workflows (e.g. data profiling, schema attribution)

**Long-term:**

- Visual and structured outputs consumed by business teams
- Feedback captured and used to improve agents (via Mem0, Phoenix Arize)

---

## 10. Open Questions / TBD

- Best pattern to trigger workflows (webhooks vs API vs event bus)?
- What UI components will offer optimal persona-guided experience?
- What parts of physical workflows will require SME guidance vs automation?
- How will versioning of agent instructions be handled?

---

## 11. Timeline and Milestones

**Goal by End of Next Week:** Run through full conceptual inception workflow with chat UI

**Goal by End of Month:** MVP complete with basic data upload, chat, and report generation

**Summer Goal:** v1 release with conceptual + physical workflows and persistent memory (Mem0 + Phoenix Arize)

---

## 12. Cursor Agent Scope Breakdown (Task-Master Enabled)

### Frontend Tasks:

*Tag: MVP unless otherwise noted*

- Build React-based login and authentication UI *(Tag: Production)*
  -   - Create login form with email/password *(Tag: Production)*
  -   - Implement client-side validation *(Tag: Production)*
  -   - Hook into backend auth/token system *(Tag: Production)*
- Create persona selector UI component
  - Dropdown with persona presets
  - Hook selection into backend context state
- Design and implement chat interface
  - Chat bubble styling, input field, streaming text updates
  - Typing indicators and message retry logic
- Upload panel for CSV, PDF, TXT
  - Drag-and-drop or file select
  - Show file status and feedback on parse success/failure
- Output rendering panel
  - Display summaries, charts, and links to documents
  - Export as PDF or .docx with one click

### Backend Tasks:

*Tag: MVP*

- Setup Flask+Node server with API routes
- File upload endpoint
  - Handle CSV/PDF parse and send to embedder
- Embed + vector memory handler
  - Generate OpenAI embeddings, send to Pinecone
- LiteLLM/OpenAI API relay
  - Forward structured prompts and receive completions
- Auth logic (JWT or session-based)

### Coordinator Agent Tasks:

*Tag: MVP*

- Session manager
  - Store session ID, persona, and stage
  - Restore prior workflows if user returns
- Intent dispatcher
  - Parse natural input and choose matching workflow
  - Dispatch webhook calls to n8n with input
- Feedback loop routing
  - If “needs clarification,” call back coaching agent
  - If “approve,” send to physical workflow stage
- Tool selector
  - Keep registry of available agents/tools
  - Fallback to defaults if no match
- Agent chaining system
  - Carry context between agents (e.g. glossary to schema tool)
  - Handle failure propagation

### n8n/Workflow Tasks:

*Tag: MVP*

- Webhook start nodes per agent
  - /start-inception, /start-glossary, etc.
- Input parser in n8n
  - Unpack JSON, match to expected agent format
- Output return node
  - Return summaries to frontend via response webhook
- Logs/markers
  - Record run context, agent names, errors if any

### Deployment Tasks:

*Tag: Beta unless otherwise specified*

- Dockerize backend (Flask/Node)
  - Write Dockerfiles, build images
- Docker Compose + Pinecone + n8n orchestration
- .env setup and variable validation
- Reverse proxy with NGINX
  - Serve `/api/` → backend, `/` → React

### Stretch Goals:

*Tag: Production/Optional*

- Phoenix Arize integration
  - Log inference traces, feedback ratings
- Feedback in chat UI
  - Add thumbs up/down or “clarify” buttons
  - Route feedback to fine-tuning vector or retraining store
- Support JSON + API data ingestion
  - User pastes URL or uploads JSON
- Developer UI panel
  - See current agent memory, vector hits, flow trace

