# V2 Dogfood Friction Log

**Date**: 2026-04-15
**Session**: V2 Core Map Experience Dogfood
**Target**: amazing-async-dev (G:\Workspace\amazing-async-dev)

---

## 1. Dogfood Results

### Scan Statistics
- Total artifacts: 55
- Projects detected: 4
  - demo-product: 9 artifacts
  - loop-journal-viewer: 21 artifacts
  - skill-pack-advisor: 17 artifacts
  - skill-pack-advisor-v1: 8 artifacts
- Parse status: 53 success, 1 partial, 1 failed

### V2 Feature Verification

| Feature | Test | Result |
|---------|------|--------|
| Project grouping | 4 projects detected | ✅ Pass |
| Timeline events | 14 events for loop-journal-viewer | ✅ Pass |
| Recent flag | All events marked is_recent (within test context) | ✅ Pass |
| Terrain regions | 6 regions per project with features | ✅ Pass |
| Terrain connections | 8 connections showing relationships | ✅ Pass |
| Status coloring | active/completed status in regions | ✅ Pass |

---

## 2. Positive Findings

| ID | Finding | Evidence |
|----|---------|----------|
| P01 | Project grouping works | 4 projects correctly identified |
| P02 | Timeline generates events | 14 events with dates |
| P03 | Terrain generates regions | 6 regions with position metadata |
| P04 | Connections show relationships | 8 feature-to-artifact connections |
| P05 | Parse success rate high | 53/55 successful parses |

---

## 3. Friction Points

| ID | Friction | Impact | V3 Candidate |
|----|----------|--------|--------------|
| F01 | No search/discovery | Cannot find artifacts by keyword | Surface F (Discovery) |
| F02 | No focus view | 17 features visible, cannot zoom to single feature detail | Surface D (Focus) |
| F03 | No narrative briefing | 15 exec results shown as flat list, no story | Surface E (Narrative) |
| F04 | Undated artifacts invisible | 24 artifacts have no date → invisible in timeline | Timeline enhancement |
| F05 | No status transition visualization | Cannot see planning→executing→completed flow | Motion language |
| F06 | Simple grid layout | Terrain uses row/col grid, not spatial positioning | Terrain enhancement |
| F07 | Static display | No motion/animation for progression | Motion language |
| F08 | Details panel limited | Shows only id/type/date, no full content | Focus view |

---

## 4. Anti-Regression Verification

| Check | Result |
|-------|--------|
| Timeline NOT flat list | ✅ Visual trail with markers |
| Timeline NOT table | ✅ CSS-based trail |
| Terrain NOT card grid | ✅ Region visualization |
| Terrain NOT table | ✅ Spatial layout (row/col) |
| Map metaphor expressed | ✅ Territory/region language |

---

## 5. V3 Scope Candidates (From Friction)

### High Priority (Core Metaphor Completion)
1. **Focus View (Surface D)** - F02, F08
   - Click region → expand to feature detail
   - Full artifact content in focus panel
   - Feature-level timeline and connections

2. **Narrative Briefing (Surface E)** - F03
   - Summarize exec history as story
   - Highlight key milestones
   - Show progression narrative

### Medium Priority (Enhancement)
3. **Motion Language** - F05, F07
   - Visual transitions for status changes
   - Animated progression indicators
   - Movement metaphor for workflow

4. **Discovery/Search (Surface F)** - F01
   - Search by keyword
   - Filter by artifact type
   - Quick find across projects

### Deferred (Requires Foundation)
5. **Spatial Terrain Enhancement** - F06
   - True spatial positioning
   - Region proximity based on relationships
   - Canvas-based map rendering

---

## 6. V3 Scope Recommendation

**Recommended**: Focus View + Narrative Briefing (2 features)

Completes the viewer experience:
- Surface A (Observatory Home) ✅ V1
- Surface B (Terrain) ✅ V2
- Surface C (Timeline Trail) ✅ V2
- Surface D (Focus View) → V3
- Surface E (Narrative) → V3

This completes the primary user journey:
1. Observatory overview → 2. Terrain map → 3. Timeline trail → 4. Focus on feature → 5. Read narrative