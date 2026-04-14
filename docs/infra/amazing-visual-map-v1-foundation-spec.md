# Amazing Visual Map V1 — Foundation Scope

## Document Control
- Project: `amazing-visual-map`
- Document Type: `V1 Foundation Scope Specification`
- Derived From: `amazing-visual-map-product-north-star-and-canonical-loop-roadmap-v2.md`
- Purpose: `Define first executable scope for autonomous canonical loop execution`
- Status: `Active`
- Autonomous Execution: `Enabled`

---

## 1. Derivation Rationale

This scope is derived from the mother document following Section 12.4 (Mandatory Self-Derivation Responsibilities) and Section 12.5 (Scope Selection Heuristics).

### 1.1 Scope Selection Criteria Applied
- **Small enough**: 3 features, ~1-2 weeks of implementation
- **Large enough**: Demonstrates real product identity (map-like observatory)
- **Identity preservation**: Keeps map metaphor, narrative awareness, interaction intent
- **Dogfoodability**: Can be used immediately on async-dev repo itself

### 1.2 Scope Anti-Regression Check
This scope explicitly avoids:
- ❌ Generic dashboard with cards/metrics/tables
- ❌ Plain file browser with sidebar tree
- ❌ Issue tracker clone
- ❌ Document index UI

This scope explicitly preserves:
- ✅ Map-like thinking (terrain, regions, landmarks metaphor)
- ✅ Observatory experience (current state pulse)
- ✅ Narrative awareness (timeline as route, not list)
- ✅ Guided understanding (recommended next action)

---

## 2. V1 Scope Definition

### 2.1 Included Features

| Feature ID | Name | Purpose | Track |
|------------|------|---------|-------|
| 001 | repo-scanner | Scan async-dev repo and extract artifacts | Core Capability |
| 002 | artifact-model | Normalize artifacts into unified data model | Information Architecture |
| 003 | observatory-home | First user-facing surface showing project state | Product Experience |

### 2.2 Intentionally Deferred

| Feature | Reason |
|---------|--------|
| Full map/terrain view | V2 - needs stable data foundation first |
| Journey/timeline view | V2 - requires temporal model |
| Focus detail view | V2 - needs core observatory first |
| Search/discovery | V2 - needs content foundation |
| Visual language system | Progressive - V1 minimal, V2 refined |
| Motion language | V2 - polish after core works |

---

## 3. Feature 001 — Repo Scanner

### 3.1 Goal
Scan a local async-dev repository and extract all canonical artifacts for downstream processing.

### 3.2 Acceptance Criteria
- AC1: Detect async-dev project structure (projects/<id>/)
- AC2: Extract feature specs from features/<id>/feature-spec.yaml
- AC3: Extract execution packs from execution-packs/*.md
- AC4: Extract execution results from execution-results/*.md
- AC5: Extract reviews from reviews/*-review.md
- AC6: Extract runstate from runstate.md
- AC7: Handle missing artifacts gracefully (partial project support)
- AC8: Output structured artifact list for downstream consumers

### 3.3 Input Contract
- Path to a local repository containing async-dev project structure
- Optional project_id filter

### 3.4 Output Contract
- List of discovered artifacts with:
  - artifact_type (feature, exec-pack, exec-result, review, runstate)
  - artifact_id
  - file_path
  - parse_status (success, partial, failed)
  - extracted_metadata (minimal: id, date, status)

---

## 4. Feature 002 — Artifact Model

### 4.1 Goal
Normalize extracted artifacts into a unified data model suitable for observatory presentation.

### 4.2 Acceptance Criteria
- AC1: Define ProjectArtifact dataclass with stable fields
- AC2: Normalize feature spec → ProjectArtifact
- AC3: Normalize exec pack → ProjectArtifact
- AC4: Normalize exec result → ProjectArtifact
- AC5: Normalize review → ProjectArtifact
- AC6: Normalize runstate → ProjectArtifact
- AC7: Extract relationships (feature ↔ exec-pack ↔ exec-result)
- AC8: Calculate minimal state summary (active count, completed count, blocked count)

### 4.3 Model Structure (V1 Minimal)
```
ProjectArtifact:
  - artifact_type: str
  - artifact_id: str
  - title: str
  - summary: str
  - date: str | None
  - status: str | None
  - feature_id: str | None
  - relationships: list[str]
  - source_path: Path
  - parse_status: str
  - metadata: dict
```

---

## 5. Feature 003 — Observatory Home

### 5.1 Goal
Provide first user-facing surface that communicates current project state using map-like presentation (not generic dashboard).

### 5.2 Experience Intent
User should feel:
- "I understand where this project currently stands."
- "I can see active regions and friction zones."
- "This feels like entering a living project map."

### 5.3 Anti-Regression Design Rules
- ❌ NO: Grid of summary cards with big numbers
- ❌ NO: Table of issues/tasks
- ❌ NO: Sidebar + main panel file browser pattern
- ✅ YES: Map-like region visualization (even minimal)
- ✅ YES: Terrain/atmosphere visual tone (dark observatory mode)
- ✅ YES: Route-based timeline hint (timeline as trail preview)

### 5.4 Acceptance Criteria
- AC1: Display project name and current state pulse
- AC2: Show active features as "regions" (visual distinction from table)
- AC3: Show recent activity as "movement trail" (not flat list)
- AC4: Show blocked items as "friction zones" (distinct visual signal)
- AC5: Provide recommended next action as "guided path hint"
- AC6: Use dark observatory visual tone (not bright admin UI)
- AC7: Load and render within 2 seconds for typical project
- AC8: Graceful handling of empty/partial projects

### 5.5 Minimal Map Metaphor Expression
V1 Observatory Home must show:
- **Current Position**: Where the project stands now (state summary)
- **Active Regions**: Where work is happening (feature clusters)
- **Recent Movement**: What happened lately (timeline trail preview)
- **Friction Zones**: Where there are blockers/issues
- **Path Hint**: What should happen next

---

## 6. Technical Direction (V1)

### 6.1 Recommended Stack
- Frontend: React + TypeScript + Tailwind CSS
- Backend: Python FastAPI (local parser service)
- Data Flow: Scanner → Model → API → Frontend

### 6.2 Architecture Principle
- Backend handles repo scanning and parsing
- Frontend handles presentation and interaction
- No database required (V1 reads from files directly)
- Local-only (no cloud, no auth, no multi-user)

### 6.3 Local Setup
- User clones repo
- Runs `npm install` + `pip install`
- Runs `npm run dev` + `python server.py`
- Opens localhost:3000
- Points UI to a local async-dev repo path

---

## 7. Product Identity Preservation Proof

### 7.1 How V1 Avoids Dashboard Drift
| Typical Dashboard | V1 Observatory Home |
|-------------------|---------------------|
| Cards with metrics | Regions with visual identity |
| Tables of items | Trail/movement visualization |
| Flat lists | Progressive disclosure |
| Bright admin UI | Dark observatory tone |
| Sidebar navigation | Map-like exploration hints |

### 7.2 How V1 Preserves Map Metaphor
- Project state → "current position" (terrain feel)
- Features → "regions" (cluster visualization)
- Activity → "movement trail" (sequence visualization)
- Blockers → "friction zones" (warning visualization)
- Next action → "path hint" (guidance visualization)

---

## 8. Validation Criteria

### 8.1 Technical Validation
- Repo scanner works on real async-dev repo (amazing-async-dev itself)
- Artifact model produces stable normalized output
- Observatory home renders without error
- Graceful handling of empty/partial projects

### 8.2 Experience Validation
- Does NOT look like generic admin dashboard
- DOES feel like entering a project observatory
- Current state is understandable in < 30 seconds
- Map metaphor is visible (not superficial styling)

### 8.3 Dogfood Validation
- Use V1 on amazing-async-dev repo
- Capture friction log
- Identify V2 improvement candidates

---

## 9. Execution Order

Recommended canonical loop sequence:
1. Feature 001 (repo-scanner) — Foundation, no UI dependency
2. Feature 002 (artifact-model) — Depends on 001
3. Feature 003 (observatory-home) — Depends on 001 + 002

Each feature → spec → execution-pack → run-day → review-night → continue

---

## 10. Escalation Conditions

Per Section 12.9, escalation only for:
- Core product metaphor change
- Major architecture shift
- Two equally strong but different design directions
- External dependency cost change

No escalation for:
- Local optimization choices
- Incremental compromises
- Design details not locked in mother document

---

## 11. Next Iteration Trigger

After V1 completion:
- Dogfood on real async-dev repo
- Capture friction and identity preservation quality
- Derive V2 scope (full map view, journey view, visual language refinement)
- Continue without interruption unless escalation triggered

---

## 12. Autonomous Execution Statement

This V1 Foundation Scope is self-derived from the mother document following Section 12 Autonomous Canonical Loop Execution Policy.

The canonical loop should proceed to:
1. Create Feature 001 spec in detail
2. Execute Feature 001 via canonical loop
3. Continue to Features 002, 003
4. Review V1 completion
5. Derive V2 scope
6. Continue iteratively

No waiting for repeated human confirmation required unless escalation condition triggered.