# Amazing Visual Map V3 — Focus & Narrative Scope

## Document Control
- Project: `amazing-visual-map`
- Document Type: `V3 Scope Specification`
- Derived From: `V2 Dogfood Friction Log`
- Purpose: `Complete viewer experience (Surfaces D + E)`
- Status: `Active`
- Autonomous Execution: `Enabled`

---

## 1. Derivation Rationale

V3 scope is derived from:
1. **Friction Log F02, F08**: No focus view - cannot zoom into feature detail
2. **Friction Log F03**: No narrative briefing - exec results shown as flat list
3. **Mother Document Section 14**: Focus View and Narrative Briefing required
4. **V2 Success**: Core map metaphor working, need completion of viewer journey

### 1.1 Scope Selection Criteria Applied
- **Small enough**: 2 features, focused on completing viewer journey
- **Large enough**: Completes primary user journey (overview→map→trail→focus→narrative)
- **Identity preservation**: Delivers the "map-like exploration" experience fully
- **Dogfoodability**: V3 will be immediately usable on amazing-async-dev

### 1.2 Anti-Regression Check
V3 must NOT:
- ❌ Become generic CRUD detail view
- ❌ Use standard form-based artifact editor
- ❌ Flat text output without narrative structure

V3 must:
- ✅ Focus view maintains map metaphor (zoom into region)
- ✅ Narrative as story/milestone sequence
- ✅ Preserve observatory dark theme identity

---

## 2. V3 Scope Definition

### 2.1 Included Features

| Feature ID | Name | Purpose | Surface |
|------------|------|---------|---------|
| 007 | focus-view | Click region → expand to feature detail with full content | Surface D |
| 008 | narrative-briefing | Summarize exec history as progression story | Surface E |

### 2.2 Intentionally Deferred

| Feature | Reason |
|---------|--------|
| Discovery/Search (Surface F) | V4 - needs viewer complete first |
| Motion Language | V4 - polish after core works |
| Spatial Terrain Enhancement | V5 - requires canvas rendering |
| Full content editor | Not in scope - viewer only |

---

## 3. Feature 007 — Focus View (Surface D)

### 3.1 Goal
Click terrain region to zoom into feature detail with full artifact content, connections, and timeline.

### 3.2 Acceptance Criteria
- AC1: Click region → focus panel expands
- AC2: Show full feature spec content (not just id/type/date)
- AC3: Show feature-related artifacts (exec packs, exec results)
- AC4: Feature-level timeline in focus view
- AC5: Back button to return to terrain
- AC6: Dark theme integration
- AC7: NO form-based editor layout
- AC8: Maintain map metaphor (zoom into region)

### 3.3 Map Metaphor Expression
- Terrain region → Zoom into district/neighborhood
- Focus panel → Street-level view
- Related artifacts → Buildings/locations in focus area

### 3.4 Anti-Regression Rules
- ❌ NOT: Standard CRUD detail view
- ❌ NOT: Form-based artifact editor
- ✅ YES: Zoom-style transition
- ✅ YES: Full content display in observatory style

---

## 4. Feature 008 — Narrative Briefing (Surface E)

### 4.1 Goal
Summarize execution history as progression story with milestones, not flat list.

### 4.2 Acceptance Criteria
- AC1: Generate narrative from exec results sequence
- AC2: Identify key milestones (completed features, blocked resolutions)
- AC3: Show progression narrative (started→progress→completed/blocked)
- AC4: Briefing appears in focus view or as separate panel
- AC5: Dark theme integration
- AC6: NO flat chronological list
- AC7: Story structure (beginning→middle→current state)

### 4.3 Map Metaphor Expression
- Exec history → Journey/travel story
- Milestones → Significant waypoints
- Narrative → Traveler's log/journal entry

### 4.4 Anti-Regression Rules
- ❌ NOT: Flat list of exec results
- ❌ NOT: Log output without structure
- ✅ YES: Story narrative format
- ✅ YES: Milestone highlighting

---

## 5. Implementation Guidance

### 5.1 Minimal Implementation Strategy
V3 focuses on **viewer completion**, not perfection:
- Focus view → Slide-in panel with full artifact content
- Narrative briefing → Text generation from exec result sequence
- Use existing observatory styling (no new theme)

### 5.2 Backend Approach
- Add `/api/focus/{project_id}/{feature_id}` endpoint
- Return feature spec + related artifacts + timeline + narrative
- Narrative generated from exec result sequence analysis

### 5.3 Frontend Approach
- Extend existing details panel to full focus view
- Add narrative section in focus panel
- CSS transition for "zoom" effect (slide-in)

---

## 6. Dogfood Validation

V3 must pass:
- Use on amazing-async-dev repo
- Focus on 17 features with full content
- Generate narrative for 15 exec results
- Complete viewer journey (overview→map→trail→focus→narrative)
- Not regress into CRUD viewer (verified by tests)

---

## 7. Escalation Check

Per Mother Document Section 12.9:
- Core product metaphor change? NO (completing, not changing)
- Major architecture shift? NO (extending V2)
- Conflicting directions? NO (friction-driven)
- External dependency? NO

**No escalation. Proceed to V3 implementation autonomously.**

---

## 8. V3 Execution Order

1. Feature 007 (focus-view) — Surface D
2. Feature 008 (narrative-briefing) — Surface E

Each → spec → implementation → tests → commit → continue

---

## 9. Success Criteria

V3 succeeds when:
- Focus view functional (click region → full content)
- Narrative briefing generated (story from exec results)
- Viewer journey complete (5 surfaces)
- Map metaphor maintained
- Dogfood on amazing-async-dev works
- No regression into CRUD viewer