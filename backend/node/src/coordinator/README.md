# Coordinator Agent Directory

This directory contains the core logic for the Coordinator Agent, responsible for orchestrating chat, persona, and workflow interactions in the backend.

## Structure

- `index.js` — Main entry point for the coordinator agent. Handles chat requests and routes them to the appropriate logic.
- `openai.js` — Handles integration with the OpenAI API for LLM-powered responses.
- `n8n.js` — Provides functions to call n8n workflows via HTTP.
- `persona.js` — Manages persona-specific system prompts and context.
- `utils.js` — Utility functions (e.g., input sanitization).
- `README.md` — This documentation file.

## Usage

Import and use the coordinator agent in your backend routes to process chat, persona, and workflow requests.

---

**Extend this directory as your agent grows in complexity!**
