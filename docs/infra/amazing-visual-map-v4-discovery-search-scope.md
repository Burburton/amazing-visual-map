# Amazing Visual Map V4 — Discovery & Search Scope

## Document Control
- Project: `amazing-visual-map`
- Document Type: `V4 Scope Specification`
- Derived From: `V3 Dogfood Friction Log`
- Purpose: `Add search/discovery utility (Surface F)`
- Status: `Active`
- Autonomous Execution: `Enabled`

---

## 1. Derivation Rationale

V4 scope is derived from:
1. **Friction Log F01**: No search/discovery - cannot find artifact by keyword
2. **Viewer Journey Complete**: Surfaces A-E implemented, F adds utility
3. **Mother Document Section 14**: Discovery/Search as utility enhancement

### 1.1 Scope Selection Criteria Applied
- **Small enough**: 1 feature, focused on utility enhancement
- **Large enough**: Adds essential navigation capability for large artifact sets
- **Identity preservation**: Maintains map metaphor in search results
- **Dogfoodability**: V4 will be immediately usable on amazing-async-dev

### 1.2 Anti-Regression Check
V4 must NOT:
- ❌ Become generic search box without map context
- ❌ Flat search results list
- ❌ Lose observatory dark theme identity

V4 must:
- ✅ Search results maintain map metaphor
- ✅ Filter by artifact type with visual indicators
- ✅ Preserve dark theme styling

---

## 2. V4 Scope Definition

### 2.1 Included Feature

| Feature ID | Name | Purpose | Surface |
|------------|------|---------|---------|
| 009 | artifact-discovery | Search artifacts by keyword, filter by type | Surface F |

### 2.2 Intentionally Deferred

| Feature | Reason |
|---------|--------|
| Motion Language | V5 - polish after core works |
| Spatial Terrain Enhancement | V5 - requires canvas rendering |
| Feature Navigation | V5 - needs discovery first |

---

## 3. Feature 009 — Artifact Discovery (Surface F)

### 3.1 Goal
Search artifacts by keyword and filter by type, with results displayed in map-like context.

### 3.2 Acceptance Criteria
- AC1: Search endpoint returns matching artifacts
- AC2: Search by keyword in title, summary, artifact_id
- AC3: Filter by artifact type (feature-spec, exec-pack, etc.)
- AC4: Results displayed with map indicators (type, status, date)
- AC5: Search results count shown
- AC6: Dark theme integration
- AC7: NO flat list without visual context
- AC8: Fast search (under 1 second)

### 3.3 Map Metaphor Expression
- Search → Scanning the terrain for locations
- Results → Points of interest matching query
- Filter → Looking for specific types of landmarks

### 3.4 Anti-Regression Rules
- ❌ NOT: Generic search box
- ❌ NOT: Flat results list
- ✅ YES: Visual search results
- ✅ YES: Type/status indicators

### 3.5 Implementation Notes
- Add `/api/search?q=keyword&type=artifact_type` endpoint
- Search in artifact.title, artifact.summary, artifact.artifact_id
- Return results with type icons, status color indicators
- Add search UI in observatory header
- CSS styling matching observatory theme

---

## 4. Implementation Guidance

### 4.1 Minimal Implementation Strategy
- Backend: Simple text search (no complex indexing)
- Frontend: Search input in header, results panel
- Results: Display with type icon, status color, date

### 4.2 Backend Approach
- Add search_artifacts() function in artifact_model
- Filter by keyword match and artifact type
- Return top 50 results with relevance score

### 4.3 Frontend Approach
- Search input in header
- Results displayed as cards with map styling
- Click result → navigate to focus view

---

## 5. Dogfood Validation

V4 must pass:
- Search on amazing-async-dev (55 artifacts)
- Find artifacts by keyword (e.g., "timeline", "journal")
- Filter by type (e.g., feature-spec only)
- Results load quickly
- Dark theme maintained

---

## 6. Escalation Check

Per Mother Document Section 12.9:
- Core product metaphor change? NO (utility enhancement)
- Major architecture shift? NO (simple search)
- Conflicting directions? NO (friction-driven)
- External dependency? NO

**No escalation. Proceed to V4 implementation autonomously.**

---

## 7. Success Criteria

V4 succeeds when:
- Search endpoint functional
- Keyword search works
- Type filter works
- Results displayed with map styling
- Dark theme maintained
- Dogfood on amazing-async-dev works