---

# GEMINI.md - Overall Structure (Template)

---

## 1. Project Overview

**Purpose:** Define what the project is and what it is not.
Clarify scope, target outcomes, primary audience, and non-goals.

---

## 2. System Role Definition

**Purpose:** Define the model's behavioral identity.
Specify role profile(s) (for example: SME, tutor, reviewer, analyst), decision boundaries, and output expectations.

---

## 3. Canonical Architecture & Governance (Single Source of Truth)

**Purpose:** Establish final authority and prevent conflicting rules.
Define precedence order across this file, code, runtime configs, and ad hoc prompts.

---

## 4. Deterministic Execution Model

**Purpose:** Define the exact stage-by-stage pipeline.

Suggested stages:
1. Conversation Intake
2. Topic Classification
3. Knowledge Integrity Check
4. Note Generation
5. Deduplication & Versioning
6. Markdown Conversion
7. Topic Folder Handling
8. Embedding
9. Retrieval Index Refresh

Define strict no-skip and no-reorder behavior.

---

## 5. Knowledge Integrity & Governance Layer

**Purpose:** Prevent knowledge base drift.

Include:
- Topic registry authority
- Topic normalization rules
- Topic fragmentation prevention
- Controlled topic expansion

---

## 6. Deduplication Policy

**Purpose:** Prevent duplicate artifacts and vector noise.
Define semantic similarity thresholds, decision classes, and audit logging requirements.

---

## 7. Versioning Policy

**Purpose:** Ensure traceability and controlled knowledge evolution.
Define immutable history, no-silent-overwrite rule, and version naming convention (`_v2`, `_v3`, archive flow).

---

## 8. Schema Versioning

**Purpose:** Future-proof structured outputs.
Require `schema_version` in every schema-governed payload and define compatibility rules.

---

## 9. Strict JSON Output Schemas

### 9.1 Topic Classification Schema

Define required keys, confidence constraints, and validation rules.

### 9.2 Note Generation Schema

Define exact machine-parseable payload prior to Markdown conversion.

For schema-governed stages, output JSON only and no extra commentary.

---

## 10. Note Format Template (Markdown Conversion Layer)

**Purpose:** Convert validated JSON into standardized Markdown artifacts.
Define mandatory sections, metadata requirements, and citation rules.

---

## 11. Auto Topic Creation

**Purpose:** Enable controlled topic expansion without taxonomy sprawl.
Define gating criteria, registry update rules, and audit trails.

---

## 12. Conversation Directory Specification

**Purpose:** Preserve raw inputs for auditability and regeneration.

Define:
- File naming convention
- Mandatory conversation JSON shape
- Non-deletion or governed-retention policy

---

## 13. Embed the Note (Vectorization Rules)

**Purpose:** Standardize chunking and embedding behavior.

Define:
- Chunk size and overlap
- Embedding provider policy
- Vector DB-only storage and metadata requirements

---

## 14. Official File Structure (Mandatory)

**Purpose:** Enforce canonical layout and avoid cross-layer leakage.
Define required directories for conversations, notes, registry, embeddings, logs, tests, and archive.

---

## 15. Official Tech Stack

**Purpose:** Lock implementation foundation and reduce drift.
Define backend, frontend, persistence, and DevOps baseline.

---

## 16. Runtime Model Configuration (Mandatory)

**Purpose:** Define provider routing and failure behavior.

Define:
- Primary model/provider route
- Secondary fallback route
- Vision and text routing logic
- Hard-fail behavior when all providers are unavailable

---

## 17. Libraries to Prefer

**Purpose:** Standardize tooling choices.
Define preferred libraries for API layer, validation, storage, parsing, and UI.

---

## 18. Error Handling & Logging Policy

**Purpose:** Prevent silent failures and improve replayability.
Define retry budget, failure classes, logging schema, and debug artifact retention.

---

## 19. Performance Guardrails

**Purpose:** Protect stability and latency under constrained resources.
Define token budgets, context headroom, concurrency limits, and response size constraints.

---

## 20. Secure Context Injection Policy

**Purpose:** Prevent uncontrolled file access and data leakage.
Define allowed paths, read-only behavior, citation requirements, and redaction rules.

---

## 21. Global Coding & Enforcement Policy

**Purpose:** Consolidate coding and quality standards.
Define language standards, naming conventions, schema validation enforcement, and CI quality gates.

---

## 22. System Philosophy (Final Authority)

**Purpose:** Establish long-term architectural intent.
Clarify deterministic behavior, traceability, versioned knowledge, and governance-first operation.

---

## 23. Context Hierarchy and Override Policy

**Purpose:** Ensure deterministic behavior across multiple context files and scopes.
Define override order for root/subdirectory policy files and conflict resolution behavior.

---

## 24. Model Version Pinning and Release Channel Policy

**Purpose:** Stabilize outputs across model updates.
Define stable/preview/experimental channel usage, pinning rules, and rollback requirements.

---

## 25. Quotas, Rate Limits, and Backpressure

**Purpose:** Preserve service quality under provider constraints.
Define RPM/TPM controls, adaptive throttling, queueing rules, and drop/defer strategy.

---

## 26. Provider Health, Circuit Breakers, and Failover SLOs

**Purpose:** Improve resilience for multi-provider operation.
Define health checks, breaker conditions, cooldown policy, and failover objectives.

---

## 27. Structured Output Validation and Auto-Repair Loop

**Purpose:** Enforce schema compliance before persistence.
Define parse/validate flow, repair attempt cap, and hard-fail behavior.

---

## 28. Context Budget and Caching Policy

**Purpose:** Improve throughput and consistency.
Define budget allocation per stage, cache key design, cache TTL, and invalidation triggers.

---

## 29. Safety Settings and Block Handling Matrix

**Purpose:** Make safety behavior explicit and predictable.
Define task-specific safety settings and blocked-output fallback behavior.

---

## 30. Audience Adaptation and Communication Policy

**Purpose:** Optimize outputs for the intended audience without binding to a single role.
Define audience profiles (for example: beginner learner, practitioner, reviewer, executive), tone, depth, and vocabulary constraints.

---

## 31. Difficulty and Detail Adaptation Policy

**Purpose:** Adjust explanation depth and complexity by context.
Define defaults when audience info is missing and escalation rules for advanced detail.

---

## 32. Mode-Specific Output Schema Extensions (Optional)

**Purpose:** Support specialized response contracts without breaking core schemas.
Define optional schema extensions for selected modes (for example: teaching mode, review mode, incident mode).

---

## 33. Interaction Quality Checks

**Purpose:** Improve usefulness through explicit verification loops.
Define checks such as comprehension checks, assumption validation, or acceptance criteria confirmation based on active mode.

---

## 34. Misunderstanding and Clarification Protocol

**Purpose:** Recover quickly from ambiguity or user confusion.
Define correction flow, clarification triggers, and concise re-explanation behavior.

---

## 35. Readability and Cognitive Load Guardrails

**Purpose:** Keep outputs digestible while preserving rigor.
Define structure constraints (chunking, short steps, recap patterns) and progressive disclosure rules.

---

## Appendix A: Implementation Checklist (Optional)

**Purpose:** Translate policy into engineering rollout tasks.
Include checklists for configuration, enforcement, tests, and go-live gates.

---

# What This Structure Achieves

- Eliminates conflicting workflow definitions
- Prevents silent corruption and schema drift
- Improves runtime stability through quotas, breakers, and validation gates
- Preserves retrieval quality via governance, deduplication, and versioning
- Supports multi-role operation without locking the system to one communication style
- Enables audience-appropriate performance while keeping deterministic behavior

---

If you want next, you can:
- Generate a minimal version (sections 1-22 only) for quick startup
- Generate a production profile (all sections with strict MUST rules)
- Generate role profiles (for example: tutor, SME, reviewer) from this template
