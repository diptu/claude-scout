---
name: sql-database-assistant
description: Helps translate natural-language data requests into correct SQL, explore and reason about database schemas, and adapt queries across MySQL, PostgreSQL, Oracle, SQL Server, DB2, SQLite, H2, and ClickHouse dialects; use when a user wants to query, inspect, or reason about a database without knowing exact SQL syntax for their engine.

# SQL Database Assistant

This skill helps Claude act as an AI-driven database client: turning plain-English questions into working SQL, exploring unfamiliar schemas, and translating queries between database dialects. Apply it whenever a user asks a question about data ("how many active users signed up last month?"), asks for a query without writing SQL themselves, pastes a schema and asks what's in it, or asks to port a query from one database engine to another.

## When to apply

- The user describes what they want to know about their data in natural language, not SQL.
- The user shares a schema (DDL, `\d` output, an ORM model, a spreadsheet of table/column names) and asks questions about it.
- The user has a working query for one engine (e.g., MySQL) and needs the equivalent for another (e.g., PostgreSQL, Oracle, SQL Server, DB2, SQLite, H2, or ClickHouse).
- The user asks Claude to review, optimize, or explain an existing SQL query.
- The user is exploring an unfamiliar database and wants a guided tour of its structure before writing queries against it.

## Step-by-step guidance

### 1. Establish the target engine first
SQL dialects diverge on pagination (`LIMIT`/`OFFSET` vs `FETCH FIRST`/`ROWNUM`/`TOP`), date functions, string concatenation, identifier quoting, and upsert syntax. Before writing a query:
- If the engine isn't stated, ask, or infer it from context (connection strings, file extensions, error messages, ORM dialect).
- Do not assume MySQL/Postgres syntax is portable — call out engine-specific choices explicitly (e.g., "using `ROWNUM` here because this is Oracle").

### 2. Understand the schema before writing SQL
- If the user hasn't shared table/column definitions, ask for them (DDL, an ER diagram description, or sample rows) rather than guessing column names.
- When a schema is provided, briefly map out the relevant tables and their relationships (primary keys, foreign keys, likely join paths) before writing the query — this catches ambiguous joins early.
- Watch for naming mismatches (singular vs. plural table names, `snake_case` vs. `camelCase`, prefixed columns) and match the user's actual schema exactly rather than idiomatic guesses.

### 3. Translate natural language into SQL deliberately
- Restate the request as a precise data question first (what's being counted/filtered/grouped, over what time window, with what edge cases like NULLs or duplicates) before writing SQL — this surfaces ambiguity ("last month" — calendar month or trailing 30 days?) while it's cheap to clarify.
- Prefer explicit, readable SQL over clever one-liners: named CTEs over deeply nested subqueries, explicit `JOIN ... ON` over implicit comma joins, explicit column lists over `SELECT *` in anything meant to be reused.
- Default to safe, non-destructive queries (`SELECT`) unless the user explicitly asks for a mutation (`INSERT`/`UPDATE`/`DELETE`/`DROP`/`ALTER`). For any mutating or schema-changing statement, flag what it will change and recommend the user run it against a backup or transaction first, especially for `DELETE`/`DROP`/`TRUNCATE`/`ALTER`.

### 4. Cross-dialect translation checklist
When porting a query between engines, check each of these before calling it done:
- **Pagination**: `LIMIT n OFFSET m` (MySQL/Postgres/SQLite/ClickHouse) vs. `FETCH FIRST n ROWS ONLY` (DB2/Oracle 12c+/SQL Server 2012+) vs. `ROWNUM`/`ROW_NUMBER()` (older Oracle) vs. `TOP n` (SQL Server).
- **String concatenation**: `||` (Oracle/Postgres/SQLite) vs. `CONCAT()` (MySQL/SQL Server) vs. `+` (SQL Server).
- **Date/time functions**: each engine has its own function names and interval syntax (e.g., `DATE_SUB`/`DATEADD`/`date('now', '-1 month')`/`INTERVAL`).
- **Identifier quoting**: backticks (MySQL) vs. double quotes (Postgres/Oracle/SQLite/H2 standard SQL) vs. brackets (SQL Server).
- **Upsert syntax**: `ON DUPLICATE KEY UPDATE` (MySQL) vs. `ON CONFLICT ... DO UPDATE` (Postgres/SQLite) vs. `MERGE` (Oracle/SQL Server/DB2).
- **Auto-increment**: `AUTO_INCREMENT` (MySQL) vs. `SERIAL`/`GENERATED ALWAYS AS IDENTITY` (Postgres) vs. `IDENTITY` (SQL Server) vs. `AUTOINCREMENT` (SQLite).
- **Column-oriented quirks (ClickHouse)**: no traditional row-level `UPDATE`/`DELETE` (use `ALTER TABLE ... UPDATE/DELETE` mutations instead), engine clauses (`ENGINE = MergeTree()`), and array/nested column types have no equivalent in row-store engines — flag when a feature doesn't translate at all rather than forcing an approximation.

### 5. Reviewing or optimizing existing queries
- Read the query for correctness first (does it answer the stated question, are joins and filters right) before suggesting performance changes.
- For performance, look for missing indexes implied by filter/join columns, unnecessary `SELECT *`, N+1 patterns if the query is generated per-row by application code, and non-sargable predicates (e.g., wrapping an indexed column in a function in the `WHERE` clause).
- Explain *why* a change helps, not just what to change — the user should be able to judge future queries themselves, not just apply this one fix.

### 6. Presenting results
- Show the SQL in a code block labeled with the target dialect.
- Briefly explain what the query does in plain language, especially any non-obvious join or filter logic.
- If the request was ambiguous and you had to make an assumption (e.g., which date column to filter on, how to treat NULLs), state the assumption explicitly so the user can correct it.
