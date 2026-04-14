# Amazing Visual Map V2 — Core Map Experience Scope

## Document Control
- Project: `amazing-visual-map`
- Document Type: `V2 Scope Specification`
- Derived From: `V1 Dogfood Friction Log`, `V1 Audit Consolidation`
- Purpose: `Complete core map metaphor (Surfaces B + C)`
- Status: `Active`
- Autonomous Execution: `Enabled`

---

## 1. Derivation Rationale

V2 scope is derived from:
1. **Friction Log F04-F07**: Missing project grouping, timeline, terrain view
2. **Audit Consolidation**: Surfaces B/C missing — core metaphor incomplete
3. **Mother Document Section 14**: Required surfaces not yet implemented

### 1.1 Scope Selection Criteria Applied
- **Small enough**: 3 features, focused on core metaphor
- **Large enough**: Completes the map identity defined in mother document
- **Identity preservation**: Delivers the core "map-like" experience
- **Dogfoodability**: V2 will be immediately usable on amazing-async-dev

### 1.2 Anti-Regression Check
V2 must NOT:
- ❌ Become a generic dashboard
- ❌ Use table-based timeline
- ❌ Flat list without sequence visualization

V2 must:
- ✅ Terrain-like visualization (even minimal)
- ✅ Trail-like timeline (movement metaphor)
- ✅ Project-level grouping (region metaphor)

---

## 2. V2 Scope Definition

### 2.1 Included Features

| Feature ID | Name | Purpose | Surface |
|------------|------|---------|---------|
| 004 | project-grouping | Group artifacts by project, enable cross-project navigation | Foundation |
| 005 | timeline-trail | Timeline visualization as movement trail (Surface C) | Journey View |
| 006 | terrain-map | Project terrain visualization (Surface B) | Map View |

### 2.2 Intentionally Deferred

| Feature | Reason |
|---------|--------|
| Focus View (Surface D) | V3 - requires core map first |
| Narrative Briefing (Surface E) | V3 - polish after core works |
| Search/Discovery (Surface F) | V3 - needs content foundation |
| Motion Language | V3 - polish phase |
| Parse failure recovery | V3 - data quality polish |

---

## 3. Feature 004 — Project Grouping

### 3.1 Goal
Group artifacts by project, enable project selection and cross-project navigation.

### 3.2 Acceptance Criteria
- AC1: Group artifacts by project_id
- AC2: Provide project list for navigation
- AC3: Filter artifacts by selected project
- AC4: Show project count in observatory header
- AC5: Project selection UI (minimal dropdown or buttons)

### 3.3 Map Metaphor Expression
- Project → World/Territory selection
- Switching projects → Moving between territories

---

## 4. Feature 005 — Timeline Trail (Surface C)

### 4.1 Goal
Visualize project history as a movement trail with sequence, not flat list.

### 4.2 Acceptance Criteria
- AC1: Display timeline as vertical/horizontal trail
- AC2: Each event as waypoint/marker on trail
- AC3: Trail shows sequence (not random ordering)
- AC4: Highlight recent movement (last 7 days)
- AC5: Click waypoint → show details
- AC6: Dark theme integration
- AC7: NO table/list format
- AC8: Load within 2 seconds

### 4.3 Map Metaphor Expression
- Timeline → Trail/Route through project history
- Events → Waypoints/Milestones on trail
- Recent activity → Movement trail segment

### 4.4 Anti-Regression Rules
- ❌ NOT: Flat chronological list
- ❌ NOT: Table of events
- ✅ YES: Visual trail with markers
- ✅ YES: Movement/sequence metaphor

---

## 5. Feature 006 — Terrain Map (Surface B)

### 5.1 Goal
Visualize project features as regions/terrain, not card grid.

### 5.2 Acceptance Criteria
- AC1: Display features as visual regions (distinct from table)
- AC2: Region color/status indicates state
- AC3: Cluster related features visually
- AC4: Show relationships as connections/paths between regions
- AC5: Zoom into region → focus view trigger
- AC6: Dark observatory terrain theme
- AC7: NO card grid, NO table format
- AC8: Graceful handling of empty/sparse projects

### 5.3 Map Metaphor Expression
- Project → Terrain/World
- Features → Regions/Districts
- Relationships → Paths between regions
- Status → Region color/atmosphere

### 5.4 Anti-Regression Rules
- ❌ NOT: Grid of feature cards
- ❌ NOT: Feature list/table
- ✅ YES: Spatial/region visualization
- ✅ YES: Map-like exploration

---

## 6. Implementation Guidance

### 6.1 Minimal Implementation Strategy
V2 focuses on **expression**, not perfection:
- Timeline trail → CSS-based vertical trail with markers (not complex animation)
- Terrain map → CSS grid/flexbox regions (not canvas rendering)
- Project grouping → Data structure + minimal UI filter

### 6.2 Frontend Approach
- Extend existing observatory HTML
- Add timeline-trail section
- Add terrain-map section
- Add project-selector UI
- CSS-only animation (no heavy JS framework)

### 6.3 Backend Approach
- Extend artifact model with project grouping
- Add timeline endpoint
- Add terrain data endpoint

---

## 7. Dogfood Validation

V2 must pass:
- Use on amazing-async-dev repo
- Visualize 55 artifacts with project grouping
- Show timeline trail of 55 events
- Show terrain of 17 features
- Not regress into dashboard (verified by tests)

---

## 8. Escalation Check

Per Mother Document Section 12.9:
- Core product metaphor change? NO (completing, not changing)
- Major architecture shift? NO (extending V1)
- Conflicting directions? NO (friction-driven)
- External dependency? NO

**No escalation. Proceed to V2 planning autonomously.**

---

## 9. V2 Execution Order

1. Feature 004 (project-grouping) — Foundation
2. Feature 005 (timeline-trail) — Surface C
3. Feature 006 (terrain-map) — Surface B

Each → spec → implementation → tests → commit → continue

---

## 10. Success Criteria

V2 succeeds when:
- Timeline trail visible (not table)
- Terrain map visible (not card grid)
- Project grouping functional
- Map metaphor expressed
- Dogfood on amazing-async-dev works
- No regression into dashboard