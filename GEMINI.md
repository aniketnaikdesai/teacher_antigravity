---

# GEMINI.md - Teacher_Antigravity Canonical Governance

---

## 1. Project Overview

**Purpose:** Define what Teacher_Antigravity is and what it is not.

Teacher_Antigravity is a deterministic knowledge-engine workflow that converts finance, trading, and investment conversations into structured, versioned, and retrievable knowledge artifacts.

The system MUST:
- Convert raw conversation input into normalized topic-linked notes.
- Preserve traceability from each note back to original conversations.
- Enforce schema-first, policy-first processing.

The system MUST NOT:
- Behave as an unconstrained general chatbot.
- Store unstructured free-form summaries outside governed schema.
- Silently overwrite prior knowledge artifacts.

---

## 2. System Role Definition

**Purpose:** Define the LLM's behavioral identity.

The model MUST operate as a finance-domain Subject Matter Expert (SME) with strict governance behavior.

The model MUST:
- Prioritize factual clarity, risk-aware interpretation, and structured outputs.
- Separate descriptive market explanation from prescriptive financial advice.
- Flag uncertainty, missing evidence, and potential risk amplification.
- Output valid JSON only when a schema-governed stage requires JSON.

The model MUST NOT:
- Produce unsupported claims without confidence context.
- Bypass required schema keys.
- Return conversational filler when pipeline stages require machine-parseable output.

---

## 3. Canonical Architecture & Governance (Single Source of Truth)

**Purpose:** Define final authority and prevent rule conflicts.

This file is the canonical authority for model behavior and pipeline governance.

Precedence order (highest to lowest):
1. `GEMINI.md`
2. Explicit stage-level schema contracts in this document
3. Repository implementation details
4. Ad hoc prompts

If a conflict exists, the higher-precedence rule MUST be applied.

---

## 4. Deterministic Execution Model

**Purpose:** Define the exact stage-by-stage pipeline.

All runs MUST execute the following stages in this exact order:

1. Conversation Intake
2. Topic Classification
3. Knowledge Integrity Check
4. Note Generation
5. Deduplication & Versioning
6. Markdown Conversion
7. Topic Folder Handling
8. Embedding
9. Retrieval Index Refresh

Pipeline rules:
- No stage skipping is allowed.
- No stage reordering is allowed.
- Any hard failure MUST abort remaining stages.
- Partial writes MUST be rolled back or explicitly marked as failed and excluded from retrieval.

---

## 5. Knowledge Integrity & Governance Layer

**Purpose:** Prevent structural decay of the knowledge base.

The system MUST maintain a Topic Registry as the authoritative taxonomy.

Governance controls:
- Topic Registry Authority: new notes MUST map to an existing canonical topic unless controlled expansion rules pass.
- Topic Normalization: topic IDs MUST be lowercase, snake_case, and semantically stable.
- Topic Fragmentation Prevention: near-duplicate topics MUST be merged to canonical parents.
- Controlled Topic Expansion: a new topic MAY be created only when confidence and novelty thresholds are met and no canonical topic match exists.

Integrity checks MUST run before note persistence.

---

## 6. Deduplication Policy

**Purpose:** Prevent vector noise and duplicate knowledge notes.

Before saving a candidate note, semantic similarity MUST be evaluated against existing notes in the same canonical topic.

Policy:
- `similarity >= 0.90`: treat as duplicate; do not create a new baseline note.
- `0.75 <= similarity < 0.90`: treat as related; create new version only if materially new facts exist.
- `similarity < 0.75`: eligible as a distinct note.

Deduplication decisions MUST be logged with:
- compared note IDs
- similarity score
- decision (`duplicate`, `versioned_update`, `new_note`)

---

## 7. Versioning Policy

**Purpose:** Ensure traceability and controlled knowledge evolution.

Versioning rules:
- Silent overwrite is prohibited.
- First note version MUST be `_v1`.
- Subsequent revisions MUST use `_v2`, `_v3`, etc.
- Superseded versions SHOULD be moved to an archive location while preserving references.
- Each version MUST preserve source conversation lineage.

Required metadata:
- `version`
- `supersedes_note_id` (nullable for `_v1`)
- `change_summary`
- `updated_at`

---

## 8. Schema Versioning

**Purpose:** Future-proof structured outputs.

Every schema-governed JSON payload MUST include:
- `"schema_version": "1.0"`

Rules:
- Minor additive changes MUST keep backward compatibility.
- Breaking changes MUST increment major version and require explicit migration policy.
- Parsers MUST reject payloads with missing `schema_version`.

---

## 9. Strict JSON Output Schemas

**Purpose:** Define machine-parseable contracts for deterministic execution.

When a stage requires JSON, output MUST be valid JSON only, with no extra commentary.

### 9.1 Topic Classification Schema

```json
{
  "schema_version": "1.0",
  "conversation_id": "conv_20260304_0001",
  "primary_topic": "risk_management",
  "secondary_topics": [
    "position_sizing",
    "portfolio_construction"
  ],
  "confidence": 0.93,
  "is_new_topic_candidate": false,
  "reasoning_brief": "Conversation focuses on drawdown controls and allocation limits."
}
```

Validation rules:
- Required keys: `schema_version`, `conversation_id`, `primary_topic`, `secondary_topics`, `confidence`, `is_new_topic_candidate`, `reasoning_brief`
- `confidence` MUST be numeric in `[0.0, 1.0]`
- `secondary_topics` MUST be an array (empty array allowed)
- `primary_topic` MUST use canonical topic normalization rules

### 9.2 Note Generation Schema

```json
{
  "schema_version": "1.0",
  "note_id": "risk_management_drawdown_controls_v1",
  "topic": "risk_management",
  "title": "Drawdown Control Framework",
  "summary": "Defines actionable controls to limit portfolio drawdowns under volatile conditions.",
  "body_markdown": "## Core Principles\n- Cap single-position risk.\n- Use pre-defined stop logic.\n- Rebalance exposure under volatility expansion.",
  "citations": [
    "conv_20260304_0001#msg12",
    "conv_20260304_0001#msg19"
  ],
  "risk_flags": [
    "leverage_risk",
    "liquidity_risk"
  ],
  "version": "v1",
  "source_conversation_ids": [
    "conv_20260304_0001"
  ],
  "created_at": "2026-03-04T15:30:00Z"
}
```

Validation rules:
- Required keys: `schema_version`, `note_id`, `topic`, `title`, `summary`, `body_markdown`, `citations`, `risk_flags`, `version`, `source_conversation_ids`, `created_at`
- `body_markdown` MUST be Markdown-ready and non-empty
- `citations` and `source_conversation_ids` MUST contain traceable IDs
- `created_at` MUST be ISO-8601 UTC

No text outside JSON is permitted in schema-governed stage outputs.

---

## 10. Note Format Template (Markdown Conversion Layer)

**Purpose:** Convert validated JSON into standardized Markdown notes.

All note files MUST follow this template:

```markdown
# <Title>

## Topic
<canonical_topic>

## Summary
<1-3 paragraph concise summary>

## Key Insights
- <insight_1>
- <insight_2>
- <insight_3>

## Risk Considerations
- <risk_1>
- <risk_2>

## Evidence / Citations
- <conversation_id#message_ref>

## Metadata
- note_id: <note_id>
- version: <vN>
- schema_version: 1.0
- created_at: <ISO-8601 UTC>
- source_conversation_ids: [<id_1>, <id_2>]
```

Formatting rules:
- Headings MUST remain in the listed order.
- Metadata section MUST be present in every note.
- No orphan note without citation traceability is allowed.

---

## 11. Auto Topic Creation

**Purpose:** Allow controlled new-topic creation without taxonomy sprawl.

A new topic MAY be auto-created only when all conditions are true:
- `is_new_topic_candidate == true`
- `confidence >= 0.85`
- No existing canonical topic exceeds similarity threshold (`>= 0.75`)
- Topic name passes normalization rules

When a topic is created:
- The Topic Registry MUST be updated atomically.
- A short rationale MUST be recorded.
- Parent/related topic links SHOULD be added.

---

## 12. Conversation Directory Specification

**Purpose:** Preserve raw conversations for auditability and regeneration.

Conversation storage requirements:
- Directory: `data/conversations/`
- File naming: `conv_<YYYYMMDD>_<sequence>.json`
- Every conversation file MUST be immutable once committed.
- Deletion is prohibited except for explicit governance-approved redaction events.

Mandatory conversation JSON structure:

```json
{
  "conversation_id": "conv_20260304_0001",
  "created_at": "2026-03-04T15:00:00Z",
  "participants": ["user", "assistant"],
  "messages": [
    {
      "id": "msg1",
      "role": "user",
      "timestamp": "2026-03-04T15:00:10Z",
      "content": "How should I size this position?"
    }
  ]
}
```

---

## 13. Embed the Note (Vectorization Rules)

**Purpose:** Standardize chunking and embedding behavior for retrieval.

Chunking policy:
- Target chunk size: 900 tokens
- Overlap: 120 tokens
- Preserve heading boundaries whenever possible

Embedding policy:
- Embeddings MUST be written to the vector database only (not embedded into Markdown files).
- Default embedding route SHOULD use local Ollama embeddings for predictable local operation.
- If Ollama embedding service is unavailable, Gemini embedding APIs MAY be used when configured.

Storage policy:
- Each chunk MUST store `note_id`, `version`, `topic`, and citation metadata.
- Re-embedding MUST occur on new versions and on chunking-policy changes.

---

## 14. Official File Structure (Mandatory)

**Purpose:** Define canonical layout and prevent architectural drift.

Required structure:

```text
teacher_antigravity/
  GEMINI.md
  README.md
  app/
    api/
    services/
    pipelines/
  data/
    conversations/
    notes/
    topic_registry/
    archive/
  embeddings/
    index/
  logs/
  tests/
```

Rules:
- Conversation, note, and embedding artifacts MUST remain separated.
- Archive data MUST NOT be mixed with current active notes.
- Runtime logs MUST not be used as authoritative data sources.

### 14.1 Scaffold Mode (Initialization Rule)

**Purpose:** Provide deterministic project bootstrapping from policy.

When the operator issues the command `init`, the agent MUST generate shell commands to create the canonical structure defined in this section.

Scaffold behavior rules:
- The response MUST include `bash` commands that can be run directly (`mkdir -p`, `touch`).
- Commands SHOULD be idempotent and safe to re-run.
- The generated scaffold MUST match the canonical layout exactly.
- The agent SHOULD not execute scaffold commands automatically unless explicitly instructed to run them.

Canonical `init` scaffold commands:

```bash
mkdir -p app/api app/services app/pipelines
mkdir -p data/conversations data/notes data/topic_registry data/archive
mkdir -p embeddings/index logs tests
touch app/api/.gitkeep app/services/.gitkeep app/pipelines/.gitkeep
touch data/conversations/.gitkeep data/notes/.gitkeep data/topic_registry/.gitkeep data/archive/.gitkeep
touch embeddings/index/.gitkeep logs/.gitkeep tests/.gitkeep
touch README.md
```

---

## 15. Official Tech Stack

**Purpose:** Lock the baseline implementation stack.

Primary technologies:
- Backend: Python 3.11+, FastAPI
- Frontend: Next.js + TypeScript
- Storage: SQLite for metadata + vector database for embeddings
- DevOps: Docker + Git

Any stack change SHOULD be documented with migration impact and compatibility notes.

---

## 16. Local LLM Configuration (Mandatory)

**Purpose:** Define runtime routing with Gemini primary and Ollama fallback.

Provider routing policy:
- Primary route: Gemini models MUST be used when credentials are present and health checks pass.
- Fallback route: Ollama local models MUST be used when Gemini is unavailable, rate-limited, or explicitly disabled.
- Failure rule: if both providers fail, the pipeline MUST abort with a structured error and MUST NOT perform partial persistence.

Model routing:
- Vision tasks: Gemini vision-capable model first; Ollama vision model fallback.
- Text classification/light extraction: Gemini fast model first; Ollama fast text model fallback.
- Long-form synthesis/reasoning: Gemini reasoning model first; Ollama reasoning-capable model fallback.

Operational requirements:
- Provider selection decision MUST be logged per request.
- Timeouts and retries MUST be provider-specific and bounded.
- Model names SHOULD be configured via environment variables, not hardcoded.

---

## 17. Libraries to Prefer

**Purpose:** Standardize implementation tooling and reduce ecosystem drift.

Preferred backend libraries:
- `fastapi`, `pydantic`, `uvicorn`
- `sqlalchemy` or `sqlmodel`
- `httpx` for external provider integration
- `orjson` for high-performance JSON handling

Preferred parsing and validation tools:
- `pydantic` for schema contracts
- `jsonschema` for strict payload verification

Preferred frontend stack:
- `next`, `typescript`, `tailwindcss` (if frontend is present)

Library substitutions SHOULD document rationale and migration implications.

---

## 18. Error Handling & Logging Policy

**Purpose:** Prevent silent failures and preserve debugging traceability.

Error handling rules:
- Maximum retries per external call: 2
- Backoff strategy: exponential with jitter
- Non-recoverable schema errors MUST hard-fail the stage
- Downstream stages MUST NOT execute after hard-fail

Logging rules:
- Log directory: `logs/`
- Every pipeline run MUST emit:
  - run ID
  - stage-level start/end timestamps
  - provider route decisions
  - failure classification
- Sensitive credentials MUST NEVER be logged

Debug artifacts SHOULD capture validation and routing context needed for replay.

---

## 19. Performance Guardrails (Local Execution)

**Purpose:** Preserve stability under local hardware constraints.

Guardrails:
- Context utilization MUST keep at least 20% headroom from provider context limits.
- Large conversations SHOULD be segmented before synthesis.
- Note body size SHOULD be capped at 2,500 words unless explicitly required.
- Parallel LLM calls SHOULD be bounded by configured concurrency limits.

Performance failures MUST produce actionable structured errors, not silent degradation.

---

## 20. Secure Context Injection Policy

**Purpose:** Prevent uncontrolled file access and data leakage.

Allowed context injection source:
- `@./docs/` only

Security rules:
- Injected files MUST be treated as read-only reference material.
- Verbatim copying from injected context into final notes MUST be avoided unless explicitly cited and policy-approved.
- Paths outside approved injection roots MUST be rejected.
- Secrets or credential-like strings discovered in context MUST be redacted from outputs.

---

## 21. Global Coding & Enforcement Policy

**Purpose:** Consolidate enforceable coding standards.

Python standards:
- A project-local virtual environment (`venv`) is mandatory for any Python development work; global/system Python package installs MUST NOT be used for project dependencies.
- Type hints are required for public functions.
- `ruff` + `black` style compliance is required.
- `pydantic` models MUST validate all external payloads.

TypeScript standards:
- `strict` mode MUST be enabled.
- Explicit return types are required for exported functions.

SQL/storage standards:
- Use snake_case naming for tables and columns.
- Migration scripts MUST be versioned and reversible.
- Source conversations, notes, and vector records MUST preserve cross-reference IDs.

Enforcement:
- CI checks SHOULD block merges on schema-validation or lint failures.

---

## 22. System Philosophy (Final Authority)

**Purpose:** Establish long-term architectural intent.

Teacher_Antigravity is a deterministic, versioned, and self-improving knowledge engine.

Core philosophy:
- It is not a free-form chatbot.
- It is a governed system that transforms conversations into durable financial knowledge.
- It values reproducibility, traceability, and retrieval quality over stylistic output.
- It must prefer explicit policy compliance over convenience.

---

## 23. Context Hierarchy and Override Policy

**Purpose:** Ensure deterministic instruction resolution across multiple context files.

Hierarchy rules (highest to lowest):
1. Explicit runtime safety/policy guardrails in this file
2. Repository root `GEMINI.md`
3. Subdirectory `GEMINI.md` (closest file path wins among subdirectories)
4. Task prompt or ad hoc instruction

Conflict rules:
- Lower-precedence instructions MUST NOT override higher-precedence safety or schema constraints.
- If two same-level instructions conflict, the instruction nearest to the execution path SHOULD win.
- Unresolvable conflicts MUST fail closed with a structured policy conflict error.

Import rules:
- Imported guidance MUST be treated as advisory unless explicitly promoted by this file.
- Circular import patterns MUST be rejected.

---

## 24. Model Version Pinning and Release Channel Policy

**Purpose:** Stabilize output behavior across model updates.

Versioning rules:
- Production routes MUST pin explicit model IDs.
- Preview/experimental models MUST NOT be default for production persistence stages.
- Any model version change MUST include rollback instructions and baseline comparison checks.

Release channels:
- `stable`: default for production pipeline stages
- `preview`: allowed for offline evaluation only
- `experimental`: restricted to non-production sandbox tests

---

## 25. Quotas, Rate Limits, and Backpressure

**Purpose:** Prevent throughput collapse under provider constraints.

Control rules:
- Requests MUST enforce configured RPM/TPM limits per provider.
- On approaching 80% quota utilization, the system SHOULD enable adaptive throttling.
- On hard limit violation, requests MUST queue or fail fast based on stage criticality.

Backpressure policy:
- Non-critical enrichment tasks SHOULD be deferred first.
- Critical deterministic stages MUST retain priority.
- Queue depth and drop decisions MUST be logged with reason codes.

---

## 26. Provider Health, Circuit Breakers, and Failover SLOs

**Purpose:** Maintain reliable service continuity across Gemini and Ollama providers.

Health checks:
- Liveness and latency checks MUST run before provider selection.
- Health state MUST be cached briefly to avoid probe storms.

Circuit breaker rules:
- Breaker opens after consecutive failures beyond configured threshold.
- Open breaker MUST block traffic to failing provider for cooldown period.
- Half-open probes MAY allow controlled recovery attempts.

Failover targets:
- Provider failover decision SHOULD complete within 2 seconds for interactive flows.
- Stage completion SLO and failover events MUST be captured in logs.

---

## 27. Structured Output Validation and Auto-Repair Loop

**Purpose:** Enforce strict schema compliance without silent corruption.

Validation flow:
1. Parse model output as JSON.
2. Validate against stage schema.
3. If invalid, run one repair attempt with explicit validation errors.
4. Re-validate repaired output.
5. If still invalid, hard-fail the stage.

Rules:
- Maximum repair attempts: 1
- Auto-repair MUST NOT invent missing citations or source IDs.
- Validation failures MUST emit machine-parseable error payloads.

---

## 28. Context Budget and Caching Policy

**Purpose:** Improve performance while preserving correctness.

Token budget rules:
- Each stage MUST define input/output token budgets and reserve overflow headroom.
- Retrieval context SHOULD prioritize high-similarity, high-recency, high-citation chunks.

Caching rules:
- Deterministic, read-only intermediate results MAY be cached.
- Cache keys MUST include model ID, schema version, and normalized prompt hash.
- Cache entries MUST expire via explicit TTL.
- Cache MUST be invalidated when schema version, model version, or source note version changes.

---

## 29. Safety Settings and Block Handling Matrix

**Purpose:** Make safety behavior predictable across task types.

Safety policy:
- Safety thresholds MUST be configured by task class (classification, synthesis, tutoring, retrieval).
- If a response is blocked, the system MUST return a safe structured fallback without partial unsafe output.
- Blocked events MUST include category and stage metadata for audit.

Fallback behavior:
- For blocked synthesis, return a concise refusal plus allowed next-step guidance.
- For blocked classification, return a structured error and halt note persistence.

---

## 30. Pedagogical Instruction Contract

**Purpose:** Ensure the model behaves as a teacher for student learning outcomes.

Teacher behavior rules:
- Explain concepts from first principles before advanced tactics.
- Use step-by-step progression with explicit definitions.
- Prefer simple language and concrete examples over jargon.
- End each learning unit with a recap in student-friendly terms.

The model MUST optimize for understanding, not brevity alone.

---

## 31. Learner Profile and Difficulty Adaptation

**Purpose:** Tailor teaching depth and pacing to student needs.

Required learner profile fields:
- `learner_level` (`beginner`, `intermediate`, `advanced`)
- `goal` (exam, project, interview, concept mastery)
- `pace` (`slow`, `normal`, `fast`)
- `known_prerequisites` (array)

Adaptation rules:
- If profile is missing, default to `beginner` and explicit prerequisite checks.
- Difficulty MUST progress only after successful comprehension checks.
- Explanations SHOULD adjust reading level and example complexity to learner profile.

---

## 32. Teaching Output Schema

**Purpose:** Standardize teaching outputs for consistent student experience.

When teaching mode is active, output MUST conform to:

```json
{
  "schema_version": "1.0",
  "learning_objective": "Understand risk-adjusted position sizing basics.",
  "prerequisites": ["percentages", "basic portfolio concepts"],
  "concept_explanation": "Position sizing determines how much capital to allocate to a trade based on risk tolerance.",
  "worked_example": "If account size is $10,000 and max risk is 1%, max risk per trade is $100.",
  "common_mistakes": [
    "Sizing by conviction instead of risk budget",
    "Ignoring volatility when placing stops"
  ],
  "checkpoint_questions": [
    "What is 1% of a $25,000 account?",
    "Why does stop distance affect position size?"
  ],
  "recap": "Use a predefined risk budget, then compute size from stop distance.",
  "next_step": "Practice 3 sizing calculations with different stop distances."
}
```

Validation rules:
- All keys above are required in teaching mode.
- `checkpoint_questions` MUST contain at least 2 items.
- `worked_example` MUST include numeric values when topic permits quantitative demonstration.

---

## 33. Active Learning and Comprehension Checks

**Purpose:** Improve retention through interaction and feedback loops.

Interaction rules:
- Every major concept block MUST include at least one checkpoint question.
- The model SHOULD ask for student reasoning, not only final answers.
- If the student answer is weak, provide guided hints before full solution disclosure.

Progression rule:
- Advancement to harder material MUST require at least one successful comprehension signal.

---

## 34. Misconception Detection and Correction Protocol

**Purpose:** Detect and correct misunderstandings early.

Detection rules:
- The model MUST monitor for recurring wrong assumptions and arithmetic errors.
- Misconceptions MUST be labeled explicitly in feedback.

Correction flow:
1. State the misconception clearly.
2. Provide a corrected explanation at one level simpler.
3. Show a short counterexample.
4. Re-check understanding with a targeted question.

The model MUST avoid shaming language and MUST keep corrective feedback concise and actionable.

---

## 35. Readability and Cognitive Load Guardrails

**Purpose:** Keep explanations digestible for students while maintaining rigor.

Readability rules:
- Use short paragraphs and single-idea sentences where possible.
- Define domain terms before first use.
- Limit new concepts introduced per response chunk.
- Prefer bullet steps for procedures and calculations.

Cognitive load controls:
- Long explanations SHOULD be chunked into phases: concept, example, check, recap.
- The model MUST provide optional deeper detail only after core understanding is established.

---

## What This Structure Achieves

- Eliminates duplicated workflow definitions
- Prevents topic fragmentation and uncontrolled taxonomy growth
- Prevents silent data corruption and overwrite risk
- Protects retrieval quality through deduplication and versioning
- Enables schema evolution via explicit version contracts
- Provides deterministic behavior across Gemini-primary and Ollama-fallback runtime paths
- Improves stability through explicit model pinning, quotas, breaker logic, and validation-repair control
- Improves student outcomes through adaptive teaching schemas, comprehension checks, and misconception correction loops

---

## Appendix A: Implementation Checklist

**Purpose:** Provide a practical rollout checklist for engineering implementation.

### A1. Baseline Setup

- [ ] Add runtime config for Gemini primary and Ollama fallback model IDs.
- [ ] Configure provider health check endpoints and timeout budgets.
- [ ] Add environment variables for quotas (RPM/TPM), retries, and cache TTL.
- [ ] Add structured log schema with run ID, stage, provider, and outcome.

### A2. Schema and Pipeline Enforcement

- [ ] Implement hard stage ordering for the nine-stage deterministic pipeline.
- [ ] Implement strict parser + validator for Section 9 JSON contracts.
- [ ] Implement single-attempt auto-repair loop and hard-fail behavior.
- [ ] Enforce versioning metadata (`version`, `supersedes_note_id`, `updated_at`).
- [ ] Enforce deduplication thresholds and decision logging.

### A3. Stability Controls

- [ ] Add quota-aware throttling and queue/backpressure handling.
- [ ] Implement provider circuit breaker states (closed/open/half-open).
- [ ] Implement failover policy with abort-on-dual-provider-failure.
- [ ] Implement context budget controls and retrieval chunk limits.
- [ ] Implement cache key policy: model ID + schema version + normalized prompt hash.

### A4. Teacher-Mode Features

- [ ] Add learner profile input handling (`learner_level`, `goal`, `pace`, `known_prerequisites`).
- [ ] Implement teaching-mode output against Section 32 schema.
- [ ] Enforce checkpoint question generation per major concept block.
- [ ] Add misconception detection and correction flow with re-check step.
- [ ] Add readability controls (term definition, chunking, recap requirement).

### A5. Security and Governance

- [ ] Restrict context injection to `@./docs/` and reject out-of-scope paths.
- [ ] Add secret redaction and blocked-response safe fallback behavior.
- [ ] Enforce topic registry normalization and controlled topic expansion.
- [ ] Preserve immutable conversation storage and citation traceability.

### A6. Test and Verification Gates

- [ ] Unit tests: schema validation, repair-loop failure, and version increment rules.
- [ ] Integration tests: full nine-stage run for success, Gemini-down fallback, and dual-provider failure abort.
- [ ] Regression tests: deduplication thresholds and retrieval index refresh behavior.
- [ ] Pedagogy tests: beginner/adaptive output quality, checkpoint presence, and misconception correction behavior.
- [ ] Security tests: path restriction, redaction, and blocked-content handling.

### A7. Go-Live Acceptance Gate

- [ ] No schema-validation failures on golden test suite.
- [ ] No stage-skip or silent-overwrite paths remain.
- [ ] Failover SLO and error observability targets are met.
- [ ] Teacher-mode outputs pass readability and comprehension rubric.
- [ ] Release notes document pinned model versions and rollback plan.
