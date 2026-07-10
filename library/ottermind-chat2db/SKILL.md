---
name: sql-database-assistant
description: Helps write, review, debug, and optimize SQL queries and database operations across MySQL, PostgreSQL, Oracle, SQL Server, DB2, SQLite, H2, ClickHouse, and other relational databases; use when the user is working with a database client, writing SQL, designing schemas, or troubleshooting query behavior.
---

# SQL Database Assistant

This skill helps with day-to-day relational database work: writing correct SQL, reviewing queries before they run against real data, exploring and explaining schemas, diagnosing slow or broken queries, and translating between different SQL dialects.

## When to apply this skill

Apply it whenever the user is:
- Writing or editing SQL (SELECT, INSERT, UPDATE, DELETE, DDL statements)
- Working with a database GUI client or CLI (e.g. connecting to MySQL, PostgreSQL, Oracle, SQL Server, DB2, SQLite, H2, or ClickHouse)
- Asking to design or modify a table schema, index, or migration
- Debugging why a query returns wrong results, errors, or runs slowly
- Asking for a query to be translated from one database dialect to another
- Asking questions about data stored in a database that require constructing a query to answer

## Step-by-step guidance

1. **Identify the database engine first.** SQL dialects diverge on pagination (`LIMIT`/`OFFSET` vs `FETCH FIRST`/`ROWNUM`), string concatenation, date/time functions, upsert syntax (`ON CONFLICT` vs `MERGE` vs `ON DUPLICATE KEY UPDATE`), and identifier quoting. Ask or infer the target engine before writing a query, and call out dialect-specific syntax explicitly in the answer.

2. **Understand the schema before writing queries.** If table/column definitions aren't already known, ask for them or ask the user to share the output of a schema-inspection command appropriate to their engine (e.g. `\d tablename` in psql, `SHOW CREATE TABLE` in MySQL, `DESCRIBE` in Oracle/SQLite). Never invent column or table names — if the schema is unknown and unavailable, say so rather than guessing.

3. **Prefer read-only queries by default.** When a user's intent is to inspect or answer a question about data, write a `SELECT` rather than a mutating statement unless they explicitly ask to change data. When a mutating statement (`UPDATE`, `DELETE`, `DROP`, `TRUNCATE`, `ALTER`) is genuinely needed:
   - Always show the corresponding `SELECT` first so the user can see which rows would be affected before running the mutation.
   - Flag any `UPDATE`/`DELETE` that lacks a `WHERE` clause as a full-table operation and confirm that's intended.
   - For destructive DDL (`DROP TABLE`, `TRUNCATE`), explicitly warn about irreversibility and suggest a backup or transaction wrapper where the engine supports it.

4. **Write for correctness first, then performance.** Get a query returning the right rows before optimizing. Common correctness pitfalls to check for: `NULL` handling in comparisons (`= NULL` vs `IS NULL`), unintended cartesian joins from a missing join condition, `GROUP BY` columns that don't match the `SELECT` list, off-by-one errors in date range filters, and duplicate rows from unintended one-to-many joins.

5. **When optimizing a slow query:**
   - Ask for or infer the query plan (`EXPLAIN`, `EXPLAIN ANALYZE`, or the engine's equivalent) rather than guessing at the bottleneck.
   - Look first for missing indexes on join/filter/sort columns, then for functions applied to indexed columns (which can prevent index use), then for unnecessary `SELECT *` pulling more data than needed.
   - Suggest the smallest change that fixes the bottleneck rather than a full query rewrite, unless the existing query is structurally wrong.

6. **When translating between dialects,** convert syntax construct by construct (data types, functions, pagination, upsert, string/date handling) and note any construct that has no direct equivalent in the target engine so the user isn't surprised by silently different behavior.

7. **When asked to design a schema or migration,** default to normalized design unless the user's access pattern clearly favors denormalization, choose explicit column types and constraints (`NOT NULL`, foreign keys, unique constraints) rather than leaving them implicit, and name indexes/constraints descriptively.

8. **Always present the final SQL in a labeled code block** noting the target dialect, so the user can copy it directly into their database client of choice.
