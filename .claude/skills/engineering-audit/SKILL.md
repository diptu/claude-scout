# 🧠 SKILL.md — Engineering Audit Skill (Skill Usage Verifier)

## 🧩 Skill Name
skill-usage-auditor-v1

## 🧠 Domain
engineering / governance / quality-assurance / system-audit

---

## 🎯 Phase Responsibility
Cross-cutting governance layer (all phases)

This skill verifies:
- correct skills were used for each phase
- no missing responsibilities in execution
- no skill misuse or overlap
- proper alignment between output and expected skill behavior

---

# 🚀 Core Objective

To ensure that:

> Every phase of the system uses the **right skill, at the right time, for the right responsibility**

It acts as the **internal compliance + architecture correctness checker** of the Claude IT Team.

---

# 🧭 Primary Responsibilities

## 1. Skill Usage Validation
Verify:
- Was the correct skill used for the task?
- Was the responsibility aligned with skill definition?
- Was the output within expected scope?

### Example:Backend Engineer implementing UX research logic → ❌ drift detected


---

# 🧪 Inputs

This skill consumes:

- Execution logs
- Phase outputs
- SKILL.md definitions
- Workflow trace data
- Role assignment map

---

# 📤 Outputs

Generates:

```text
audit_report.md
skill_violation_report.json
coverage_matrix.json
recommendations.md
🧠 Audit Rules
Rule 1 — Strict Ownership

Every task must have exactly one responsible skill.

Rule 2 — No Silent Failures

Missing skill execution = critical failure.

Rule 3 — Scope Boundaries Matter

Skills must not exceed their domain definition.

Rule 4 — Evidence Required

Every audit decision must be backed by:

logs
outputs
SKILL.md contract
⚔️ Evaluation Metrics
Metric	Weight
Detection accuracy	30%
Scope correctness	25%
Coverage completeness	20%
False positive control	15%
Recommendation quality	10%
🚨 Failure Modes

This skill must avoid:

assuming missing data without evidence
misclassifying valid cross-skill collaboration
over-restricting natural system flexibility
ignoring context of multi-skill workflows
🧩 Dependencies

Relies on:

all SKILL.md definitions
execution logs from Claude Scout
phase outputs (PRDs, architecture, etc.)
system traceability layer
🔁 Position in System
All Phases Execution
        ↓
   Skill Usage Logs
        ↓
  🔍 Audit Skill (THIS)
        ↓
Violation / Approval Report
        ↓
   System Improvement Loop
🏆 Success Criteria

Audit is successful when:

incorrect skill usage is detected reliably
missing responsibilities are flagged
system improves over time based on findings
no silent misalignment exists in execution
🧠 Philosophy

“A system is only as strong as its enforcement of role boundaries.”

This skill ensures architectural discipline across the entire Claude IT Team.

🔄 Version

v1.0 — Claude Scout Governance & Audit System


---

If you want next upgrades, I can build:

- 🧠 **Auto-Fix Auditor (suggests correct skill replacements)**
- ⚔️ **Skill Battle Auditor (compares competing skills usage)**
- 📊 **Org-wide compliance dashboard**
- 🔁 **Self-healing Claude IT system loop**

