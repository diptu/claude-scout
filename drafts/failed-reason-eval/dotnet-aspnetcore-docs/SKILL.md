---
name: aspnet-core-helper
description: Assists with ASP.NET Core web application development (routing, middleware, dependency injection, configuration, minimal APIs, and common project conventions); use whenever a user is building, debugging, or reviewing an ASP.NET Core project.
---

# ASP.NET Core Helper

This skill helps with building, debugging, and reviewing ASP.NET Core applications: minimal APIs and MVC controllers, middleware pipelines, dependency injection, configuration, and common project structure decisions.

## When to apply this skill

Apply this skill whenever the user is:
- Writing or modifying an ASP.NET Core project (`Program.cs`, `Startup.cs`, controllers, minimal API endpoints, Razor Pages, Blazor server/wasm hosting).
- Debugging routing, middleware ordering, dependency injection lifetime issues, or configuration binding problems.
- Asking about ASP.NET Core conventions (project layout, `appsettings.json` structure, environment-specific configuration).
- Reviewing ASP.NET Core code for correctness against framework idioms (e.g. proper use of `IHostedService`, `IOptions<T>`, `ILogger<T>`).

## Core guidance

### 1. Program.cs and the hosting model
- Modern ASP.NET Core (6.0+) uses the minimal hosting model in `Program.cs`: `WebApplication.CreateBuilder(args)` to configure services, `builder.Build()` to create the app, then `app.Map...`/`app.Use...` calls before `app.Run()`.
- Older or migrated projects may still split configuration into `Startup.cs` with `ConfigureServices` and `Configure` methods — recognize both patterns and don't assume one over the other without checking the project's actual files first.
- Service registration happens on `builder.Services` (an `IServiceCollection`); middleware registration happens on `app` after `Build()`. Don't mix these up — a common bug is trying to register middleware before the app is built, or trying to add services after it is.

### 2. Middleware pipeline ordering
- Middleware order matters and executes in the order registered, then unwinds in reverse. Common correct ordering: exception handling → HTTPS redirection → static files → routing → CORS → authentication → authorization → custom middleware → endpoint mapping.
- Authentication middleware (`UseAuthentication`) must come before authorization middleware (`UseAuthorization`), and both must come after `UseRouting` but before endpoint mapping (`MapControllers`, `MapGet`, etc.).
- When debugging "middleware doesn't seem to run" or "user is authenticated but still gets 401/403," check the order first before checking the middleware's own logic.

### 3. Dependency injection lifetimes
- Three lifetimes: `Transient` (new instance every request for the service), `Scoped` (one instance per HTTP request), `Singleton` (one instance for the app's lifetime).
- A common bug class: injecting a `Scoped` service into a `Singleton` (e.g. a background service) — this throws at runtime or silently captures a stale instance. If a singleton needs a scoped dependency (like a `DbContext`), it must create a scope manually via `IServiceScopeFactory` per operation, not take the scoped service directly in its constructor.
- Prefer constructor injection. Only reach for `IServiceProvider` directly (service locator pattern) when the dependency truly can't be known at construction time.

### 4. Minimal APIs vs. controllers
- Minimal APIs (`app.MapGet("/route", handler)`) suit small services and simple CRUD endpoints; MVC controllers (`[ApiController]` + `ControllerBase`) suit larger APIs needing model binding attributes, action filters, or conventional routing across many endpoints.
- Don't recommend converting an entire controller-based project to minimal APIs (or vice versa) unless the user asks — treat this as a deliberate architectural choice, not a default cleanup.
- Both support the same DI, model validation, and filter pipeline concepts; only the registration syntax differs.

### 5. Configuration and options
- Configuration is layered: `appsettings.json` → `appsettings.{Environment}.json` → environment variables → command-line args, each overriding the previous. `ASPNETCORE_ENVIRONMENT` controls which environment-specific file loads.
- Bind configuration sections to strongly-typed classes via `builder.Services.Configure<TOptions>(builder.Configuration.GetSection("SectionName"))`, then inject `IOptions<TOptions>` (or `IOptionsSnapshot<TOptions>` for per-request reload in scoped contexts) rather than reading `IConfiguration` directly inside business logic.
- Never suggest committing secrets (connection strings, API keys) into `appsettings.json` — point to user secrets (`dotnet user-secrets`) for local development and environment variables or a secret manager for production.

### 6. Common project structure
- Typical layout: `Program.cs` at the root, `Controllers/` or `Endpoints/` for request handling, `Models/` or `Dtos/` for data shapes, `Services/` for business logic, `Data/` for `DbContext` and EF Core migrations.
- When reviewing or scaffolding a project, match the existing structure rather than imposing a different convention — check how the project currently organizes files before adding new ones.

## Step-by-step approach when helping with a task

1. Identify the ASP.NET Core version and hosting model in use (minimal hosting vs. `Startup.cs`) by checking `Program.cs` and the `.csproj` target framework before writing any code.
2. Identify whether the project uses minimal APIs, MVC controllers, or both, and follow the existing pattern.
3. For bugs involving middleware behavior (auth, CORS, routing), trace the actual middleware registration order in `Program.cs`/`Startup.cs` before proposing a fix.
4. For DI-related errors, check the lifetime of every service in the failing chain (constructor injection graph) — most "unable to resolve service" or "cannot consume scoped service from singleton" errors trace back to a lifetime mismatch.
5. When adding configuration, bind it through the options pattern rather than reading `IConfiguration["Key"]` scattered across the codebase.
6. Prefer the smallest change that fits the project's existing conventions over introducing a new pattern (e.g. don't introduce a new DI container, a new configuration library, or a different API style without being asked).
