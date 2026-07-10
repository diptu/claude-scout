---
name: react-admin-crud-scaffold
description: Scaffolds admin/back-office single-page apps backed by REST or GraphQL APIs, generating list/edit/create/show views with sorting, filtering, pagination, validation, and auth out of the box; use when a user needs an internal admin panel or CRUD dashboard for managing records from an existing API rather than a public-facing UI.
---

# React-Admin CRUD Scaffold

## What this skill helps with

Building admin panels and internal back-office tools that let non-technical staff view, search, filter, create, edit, and delete records exposed by a REST or GraphQL API. Instead of hand-rolling tables, forms, and pagination for every resource, this skill applies a declarative, resource-oriented pattern (in the style of react-admin) where each entity in the API gets a `<Resource>` definition composed of `list`, `edit`, `create`, and `show` views built from small declarative field/input components.

This is for internal tooling and admin dashboards, not customer-facing product UI — the priority is speed of development and consistency across resources, not bespoke visual design.

## When Claude should apply this

- The user asks for an "admin panel," "back office," "internal dashboard," or "CRUD UI" for an existing API.
- The user wants to manage database records (users, orders, products, etc.) through a web UI without writing a full custom frontend.
- The user has a REST or GraphQL API already and needs a management layer on top of it, in React with TypeScript.
- The user mentions needing list/table views with sorting, filtering, and pagination, paired with create/edit forms and validation, for multiple resource types.

Do not apply this for public-facing marketing sites, complex bespoke UX flows, or apps where the primary API is not resource/CRUD-shaped (e.g., a single-page calculator or a chat interface).

## Step-by-step guidance

1. **Identify the resources.** List every entity the admin needs to manage (e.g., `users`, `orders`, `products`). Each becomes one resource with its own list/create/edit/show views.

2. **Define a data provider contract first.** Before building UI, nail down how the frontend talks to the API: base URL, auth (bearer token / cookie), and the exact shape of list responses (does the API return total count via a header or a body field? what does pagination look like — page/perPage or offset/limit?). Mismatches here cause the most bugs, so confirm this contract before writing components.

3. **Scaffold per-resource views using a consistent shape:**
   - **List view**: a table with columns mapped to fields, built-in sort-by-column, pagination controls, and a filter bar (text search, date range, select filters) that maps to query params/GraphQL variables.
   - **Edit/Create view**: a form built from typed input components (text, number, select, reference/autocomplete for foreign keys, date picker, boolean toggle), with client-side validation (required fields, format checks) mirroring the API's validation rules.
   - **Show view**: a read-only detail layout for a single record, useful when edit permissions are restricted.

4. **Handle relationships explicitly.** For foreign keys (e.g., an order's `customerId`), use a reference input/field that fetches and displays the related record's label (name/title) instead of a raw ID, both in list columns and in edit forms.

5. **Wire up authentication and authorization.** Gate the whole admin app behind a login screen backed by the API's auth endpoint, and conditionally hide/disable actions (delete, edit) based on the current user's role/permissions returned by the API.

6. **Keep resource definitions declarative and centralized.** Register all resources (name, icon, list/edit/create/show components) in one top-level app file so the set of manageable entities is visible at a glance, rather than scattered across routing config.

7. **Add cross-cutting affordances once, not per-resource:** a consistent notification/toast system for save/delete success and error feedback, a confirm dialog before destructive actions (delete), and optimistic UI updates for edits where the API supports it — implement these as shared utilities used by every resource, not duplicated per view.

8. **Validate against the real API early.** Before considering a resource "done," exercise its list, create, edit, and delete flows against the live (or a representative mock of the) API to confirm data shapes, pagination, and error responses are handled correctly — admin panels break most often on edge cases like empty lists, validation errors, and permission-denied responses.
