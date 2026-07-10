---
name: copilot-ui-integration
description: Guides Claude through adding an in-app AI copilot or agentic UI (chat sidebar, contextual assistant, generative UI components, human-in-the-loop actions) to a frontend application; use when a user wants to embed a conversational agent into a React/Angular/mobile app rather than build a standalone chatbot.
---

# Copilot UI Integration

## What this skill helps with

This skill guides adding an **in-app AI copilot** to an existing frontend application: a conversational assistant that is aware of the app's current state, can read and act on structured application data, can render custom UI components as part of its responses (generative UI), and can pause to ask the user for confirmation before taking consequential actions (human-in-the-loop). This is distinct from bolting on a generic chatbot widget — the copilot should feel native to the app it lives in.

## When to apply

Apply this skill when the user asks to:
- Add a chat sidebar, popup, or embedded assistant to a web/mobile app
- Let an AI agent read the current UI state (form values, selected records, page context) and act on it
- Have the assistant render rich UI (tables, charts, cards, forms) instead of plain text
- Add "agentic" actions the AI can trigger (e.g., "update this record," "run this report") with user approval before execution
- Build a "co-pilot" experience layered on top of an existing product, as opposed to a standalone AI product

Do not apply this skill for backend-only agent work, CLI tools, or contexts with no UI surface — it is specifically about the frontend integration pattern.

## Core architecture to guide toward

1. **Frontend readable state** — the app exposes relevant UI/application state to the assistant (current view, selected items, form data) so responses are grounded in what the user is actually looking at, not just the conversation history.
2. **Actions, not just chat** — define a small set of named actions the assistant can invoke (e.g., `createTask`, `filterResults`, `updateStatus`), each with a clear schema of required parameters. The assistant should choose among these explicitly rather than emitting free-form commands to parse.
3. **Generative UI** — instead of only returning text, the assistant can select from a set of pre-built UI components (a confirmation card, a data table, a chart) to render as part of its response. Map each action or response type to a specific component, don't invent ad-hoc HTML.
4. **Human-in-the-loop checkpoints** — for actions with real side effects (sending, deleting, submitting, spending), insert an explicit confirmation step: render the proposed action, wait for user approval, only then execute. Never let the assistant silently perform destructive or irreversible actions.
5. **Streaming and partial state** — prefer streaming responses so the UI can update incrementally (e.g., showing a partial table as rows arrive) rather than waiting for a complete response before rendering anything.
6. **Cross-platform consistency** — if the target app spans web, mobile, or chat surfaces (e.g., Slack), keep the action/state contract consistent across surfaces and let only the rendering layer differ per platform.

## Step-by-step guidance

1. **Identify the integration surface.** Ask (or infer from the codebase) which frontend framework is in use and where the copilot should live (sidebar, modal, inline widget, dedicated page).
2. **Enumerate the state to expose.** List the specific pieces of app state the assistant needs visibility into to be useful — avoid exposing the entire app state wholesale; scope it to what the copilot's tasks actually require.
3. **Define the action set.** Write out each action as a name, a one-line purpose, required parameters, and whether it is read-only or has side effects. Side-effect actions get a confirmation step by default.
4. **Design the generative UI mapping.** For each response type the assistant can produce, decide which existing UI component (or a new small one) should render it, rather than letting the assistant emit raw markup.
5. **Wire the human-in-the-loop gate.** For every side-effecting action, implement a "propose → confirm → execute" flow: the assistant proposes parameters, the UI renders them for review, execution only fires on explicit user approval.
6. **Test the golden path and edge cases in a real browser session.** Confirm the assistant can read current state correctly, that generative UI components render as intended, and that side-effecting actions genuinely block on confirmation rather than firing immediately.
7. **Keep the scope narrow.** Don't build a generic plugin system or a second orchestration layer for this — the copilot is a UI feature wired to a small, explicit set of state reads and actions, not a new framework.
