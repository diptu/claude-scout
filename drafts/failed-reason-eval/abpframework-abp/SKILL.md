---
name: aspnet-core-modular-architecture
description: Guides Claude through structuring an ASP.NET Core enterprise application using a modular, layered, domain-driven design similar to the ABP Framework, for use when a user is building, extending, or refactoring a .NET business application that needs clean separation between domain logic, application services, data access, and UI/API layers.
---

# ASP.NET Core Modular Architecture

This skill helps design and implement enterprise-grade ASP.NET Core applications using a well-tested layered, modular, domain-driven architecture pattern (as popularized by frameworks like ABP). Apply it when a user is starting a new .NET business application, adding a new module or feature to an existing layered .NET solution, or refactoring a monolithic controller/service into cleaner boundaries.

## When to apply this skill

- The user is scaffolding a new ASP.NET Core project intended to grow into a multi-feature business application (not a small script or single-file API).
- The user asks how to organize domain logic, services, repositories, or DTOs in a .NET codebase.
- The user wants to add cross-cutting concerns (authorization, multi-tenancy, auditing, validation) in a consistent, reusable way.
- The user is splitting an existing application into independent modules that can be developed, tested, or deployed somewhat separately.
- The user mentions "clean architecture," "DDD," "application services," or "layered architecture" in a .NET context.

Do not force this structure onto small utilities, prototypes, or single-purpose scripts — the value comes from managing complexity in larger, longer-lived applications.

## Core architectural layers

Guide the user toward separating code into these conceptual layers, whether as separate projects/assemblies or as clearly namespaced folders within one project:

1. **Domain layer** — entities, value objects, domain services, and repository interfaces. Contains business rules and invariants. Has no dependency on data access technology or web frameworks.
2. **Application layer** — application services (use-case orchestrators) that coordinate domain objects, enforce authorization, and map between entities and DTOs. Application services should be thin: validate input, call domain logic, return a DTO — not contain business rules themselves.
3. **Data access / infrastructure layer** — repository implementations, database context, migrations, and integrations with external systems. Implements the interfaces defined in the domain layer.
4. **Web / HTTP API layer** — controllers (or minimal API endpoints) that expose application services over HTTP, plus request/response models. Controllers should be thin pass-throughs to application services, not contain logic.
5. **UI layer** (if applicable) — Razor Pages, MVC views, Blazor components, or a separate SPA — consumes the HTTP API or application services directly, never the domain/data layers directly.

When creating new features, walk through each layer in order (domain → application → data access → web) so dependencies flow inward toward the domain, never outward.

## Concrete step-by-step guidance

When asked to add a new feature or entity to a layered .NET application:

1. **Define the domain entity first.** Identify its identity, properties, and any invariants (e.g., "an Order must have at least one line item"). Put validation of these invariants in the entity or a domain service, not in a controller.
2. **Define a repository interface** in the domain layer describing how the entity is persisted and queried (e.g., `IOrderRepository` with methods like `GetByIdAsync`, `FindActiveOrdersAsync`). Keep the interface expressed in domain terms, not raw SQL/queries.
3. **Create DTOs** for input and output shapes (e.g., `CreateOrderDto`, `OrderDto`). Never expose entities directly over the API — this avoids leaking persistence details and over-posting vulnerabilities.
4. **Write the application service** that implements the use case: accepts a DTO, loads/validates via the repository and domain entity, applies the operation, persists changes, and returns a result DTO. Add authorization checks here (e.g., "does this user have permission to create an order?").
5. **Implement the repository** against the chosen data store (e.g., EF Core `DbContext`), keeping query logic out of the application service.
6. **Expose the application service** via a thin controller or minimal API endpoint. The endpoint should do argument binding and call the application service — nothing more.
7. **Add cross-cutting concerns consistently** rather than ad hoc per feature:
   - Authorization: check permissions in the application layer using a consistent permission-naming scheme (e.g., `OrderManagement.Orders.Create`).
   - Validation: use data annotations or a validation library on DTOs for input shape; keep business-rule validation in the domain.
   - Auditing: record created/modified timestamps and user IDs at the data access layer so every entity gets this uniformly.
   - Multi-tenancy (if relevant): filter all queries by a tenant identifier at the data access layer so no application service has to remember to do it manually.

## Modularity guidance

When a codebase is growing large enough to split into modules:

- Group each module's domain, application, and data-access code together by feature area (e.g., `Modules/Identity`, `Modules/Catalog`, `Modules/Orders`) rather than by technical layer (e.g., avoid one giant `Controllers/` folder for the whole app).
- Each module should expose its application services and DTOs as its public surface; other modules should depend on those, not reach into another module's entities or database tables directly.
- Keep shared cross-cutting infrastructure (auth, logging, base entity classes) in a common module that all feature modules depend on, but that itself depends on nothing feature-specific.

## Red flags to point out

- Controllers containing business logic or direct database queries — push this down into application services and repositories.
- Entities being returned directly from API endpoints — introduce DTOs.
- Business rule validation scattered across controllers, services, and the database — consolidate it in the domain layer.
- One module's code directly querying another module's database tables — this couples modules and defeats the purpose of splitting them; go through the other module's application service instead.
- A "God" application service that handles unrelated use cases — split by use case/feature instead.
