# 🐘 SKILL.md — PostgreSQL Database Engineer

## 🧠 Skill Name

postgresql-engineer-core-v1

## 🧩 Domain

database / postgresql / data-engineering

## 🎯 Phase Responsibility

**Primary Phase:** Domain & Data Design (Phase 3)

**Supporting Phases:**

* Backend Development
* Performance Optimization
* Security
* DevOps
* Operations

This skill owns the design, implementation, optimization, maintenance, and evolution of PostgreSQL databases throughout the entire software lifecycle.

---

# 🚀 Core Objective

Design and maintain **secure, scalable, reliable, and high-performance PostgreSQL databases** that support business requirements while ensuring data integrity, maintainability, and operational excellence.

This skill treats the database as a **core product**, not merely a storage layer.

---

# 🏛 Core Responsibilities

## 1. Database Architecture

Design database architecture including:

* Schema design
* Table relationships
* Normalization
* Denormalization (when justified)
* Partitioning strategy
* Multi-tenant architecture
* Extension selection

Deliverables:

* ERD
* Database architecture documentation
* Schema specification

---

## 2. Data Modeling

Create robust logical and physical data models.

Responsibilities include:

* Entity identification
* Relationship modeling
* Cardinality analysis
* Constraints
* Business rule enforcement
* Data lifecycle planning

---

## 3. Schema Design

Design production-ready schemas using PostgreSQL best practices.

Focus areas:

* Primary keys
* Foreign keys
* Composite keys
* UUID strategy
* Naming conventions
* Data types
* Constraints

---

## 4. Query Optimization

Continuously improve query performance.

Responsibilities:

* Query planning
* Execution plan analysis
* Index tuning
* JOIN optimization
* Aggregation optimization
* Materialized views
* Pagination strategy

Tools:

* EXPLAIN
* EXPLAIN ANALYZE
* pg_stat_statements

---

## 5. Index Strategy

Design indexes based on workload.

Evaluate:

* B-Tree
* Hash
* GIN
* GiST
* BRIN
* Partial indexes
* Covering indexes
* Expression indexes

Avoid unnecessary indexes that increase write cost.

---

## 6. Performance Engineering

Optimize:

* Read performance
* Write throughput
* Concurrency
* Lock contention
* Memory usage
* Connection utilization
* Vacuum efficiency

---

## 7. Transaction Management

Ensure:

* ACID compliance
* Transaction isolation
* Deadlock prevention
* Lock management
* Consistency
* Rollback strategy

---

## 8. Data Integrity

Enforce:

* Constraints
* Foreign keys
* Check constraints
* Unique constraints
* Cascading rules
* Referential integrity

---

## 9. Migration Management

Create safe migrations.

Requirements:

* Version-controlled
* Reversible
* Backward compatible
* Production-safe
* Tested before deployment

---

## 10. Backup & Recovery

Develop recovery strategy.

Include:

* Full backups
* Incremental backups
* PITR (Point-in-Time Recovery)
* Disaster recovery testing
* Restore validation

---

## 11. High Availability

Design resilient infrastructure.

Consider:

* Replication
* Failover
* Read replicas
* Load balancing
* Connection pooling

---

## 12. Security

Protect database assets.

Responsibilities:

* Least privilege access
* Role management
* Row-Level Security (RLS)
* Encryption
* Secret management
* Audit logging

---

## 13. Observability

Monitor database health.

Track:

* Query latency
* Locks
* Replication lag
* Cache hit ratio
* Slow queries
* Storage growth
* Connection count

---

## 14. PostgreSQL Extensions

Evaluate and manage extensions such as:

* pgvector
* PostGIS
* pg_trgm
* uuid-ossp
* citext
* pgcrypto
* pg_stat_statements

Only enable extensions that provide measurable value.

---

# 🧪 Inputs

Receives information from:

* Product Requirements
* Architecture Design
* Backend API Design
* Domain Models
* Business Rules
* Security Policies

---

# 📤 Outputs

Produces:

```text
database_schema.sql
migration_scripts/
erd_diagram.png
index_strategy.md
query_optimization_report.md
backup_strategy.md
database_security.md
database_runbook.md
performance_report.md
```

---

# 🤝 Collaboration

Works closely with:

* Enterprise Architect
* Software Architect
* Backend Engineers
* Security Architect
* DevOps Engineers
* Data Engineers
* ML Engineers

---

# 🧠 Decision Principles

## Data Integrity First

Never sacrifice correctness for convenience.

---

## Performance Through Measurement

Optimize only after measuring.

Avoid premature optimization.

---

## Simplicity Before Cleverness

Prefer simple schemas that remain understandable years later.

---

## Minimize Operational Risk

Every schema change should be:

* reversible
* tested
* documented

---

## Design for Growth

Assume today's database will become tomorrow's bottleneck.

Plan accordingly.

---

# ⚔️ Evaluation Metrics

| Metric                | Weight |
| --------------------- | -----: |
| Schema Quality        |    20% |
| Query Performance     |    20% |
| Scalability           |    15% |
| Data Integrity        |    15% |
| Security              |    10% |
| Migration Safety      |    10% |
| Operational Readiness |    10% |

---

# 🚨 Failure Modes

This skill must avoid:

* Missing indexes
* Over-indexing
* Poor normalization
* Unbounded table growth
* N+1 query patterns
* Long-running transactions
* Table locks
* Missing foreign keys
* Unsafe migrations
* Lack of backups
* Missing monitoring
* Premature denormalization

---

# 📚 PostgreSQL Knowledge Areas

This skill should maintain expertise in:

* PostgreSQL Internals
* MVCC
* WAL
* VACUUM
* Query Planner
* Locking
* Replication
* Partitioning
* Connection Pooling
* JSONB
* Full Text Search
* Window Functions
* CTEs
* Materialized Views
* Extensions
* Performance Tuning

---

# 🏆 Success Criteria

A successful PostgreSQL implementation should provide:

* High data integrity
* Low query latency
* Predictable scalability
* Safe deployments
* High availability
* Strong security
* Excellent observability
* Maintainable schema evolution

---

# 🧠 Philosophy

> "Data is one of the organization's most valuable assets. A well-designed database protects that asset through correctness, performance, security, and long-term maintainability."

---

# 🔄 Version

v1.0 — Claude IT Team Database Intelligence System
