# Phase 2 Memory-Map Integration Dogfood & Friction Log

**Date**: 2026-04-15
**Phase**: Phase 2 (Visual History, Memory Trail, Journey Guidance)
**Features**: 013, 014, 015
**Status**: Complete - Assessing continuation

---

## 1. Dogfood Results

### Feature Verification

| Feature | Tests | Dogfood | Status |
|---------|-------|---------|--------|
| Visual History (013) | 8 | ✅ Verified via API | Complete |
| Memory Trail (014) | 7 | ✅ Verified via timeline waypoints | Complete |
| Journey Guidance (015) | 9 | ✅ Verified via Recommended Path | Complete |

### Visual History Verification (Feature 013)
- Timeline waypoints have narrative section in focus panel
- Narrative text generated from timeline events
- API returns narrative: "This feature began with..."
- Timeline shows progression with status indicators

### Memory Trail Verification (Feature 014)
- Timeline waypoints show project evolution
- Waypoints have dates for evolution tracking
- Trail items clickable
- Timeline connected to terrain regions

### Journey Guidance Verification (Feature 015)
- Recommended Path adapts to state:
  - "Continue active work" when items in progress
  - "All items complete - ready for review" when completed
- Location context in focus panel
- Cross-surface continuity preserved

---

## 2. API Verification

### Focus API Response (Feature 004-v1-1-stability)

```json
{
  "feature": { "id": "004-v1-1-stability", "name": "V1.1 Stability...", "status": "active" },
  "related_features": [
    { "id": "001-artifact-reader", "name": "Artifact Reader", "status": "active" },
    { "id": "002-timeline-viewer", "name": "Timeline Viewer", "status": "active" },
    ...
  ],
  "timeline": [
    { "id": "exec-20260414-001", "date": "2026-04-14", "title": "Execute: V1.1...", "is_recent": true }
  ],
  "narrative": "This feature began with exec-20260414-001 on 2026-04-14..."
}
```

All Phase 2 fields present: narrative, timeline with titles, related_features.

---

## 3. Friction Items

| ID | Friction | Phase 2 Impact | Resolution |
|----|----------|----------------|------------|
| F08 | Narrative text-only | ✅ RESOLVED | Narrative now in focus panel with timeline |
| F09 | Feature region click not triggering focus | ✅ RESOLVED | Fixed - added onclick handler and showFocus() |
| F10 | Timeline waypoint shows artifact, not feature | ⚠️ Partial | Shows artifact details, feature focus via region click |

### F09 Resolution Details

**Root cause**: Region div had no onclick handler (only trail-items had).

**Fix**: 
1. Added `onclick="showFocus('${f.id}', '${f.title}')"` to region template
2. Created `showFocus()` async function that calls `/api/focus/{project_id}/{feature_id}`
3. Added CSS for timeline-section, related-feature, waypoint styling

**Verification**: 
- Click region → focus panel opens with feature narrative
- Click related feature → navigates to new focus view
- Timeline shows with titles and dates

---

## 4. Map Metaphor Preservation

| Metaphor Word | Present |
|---------------|---------|
| narrative | ✅ (in focus API) |
| trail | ✅ (timeline waypoints) |
| journey | ✅ (Recommended Path) |
| history | ✅ (visual history tests) |
| memory | ✅ (memory trail tests) |

All Phase 2 metaphor words present. Memory-map identity intact.

---

## 5. Test Summary

- Phase 1: 169 tests
- Phase 2: 25 tests
- **Total: 194 tests passing**

---

## 6. Diminishing Returns Assessment

**Phase 2 delivered:**
- Narrative integrated with timeline (Feature 013)
- Memory trail visual connection (Feature 014)
- Journey guidance adapts to state (Feature 015)
- 25 new tests, comprehensive coverage

**Remaining friction (F09):**
- Feature region click not triggering focus
- This is a BUG, not polish scope

**Assessment: Phase 2 nearly complete, but F09 bug needs fix.**

---

## 7. Recommendation

**FIX F09 (feature region click bug) before closing Phase 2.**

Justification:
- Feature navigation is incomplete if users can't click terrain regions
- This is a functional bug, not polish churn
- Fix maintains Phase 2 scope boundary

**After F09 fix:**
- Assess Phase 3 candidates
- Phase 3 would need clear value over Phase 2

---

## 8. Next Steps

1. Investigate F09 - why region click doesn't trigger focus
2. Fix in observatory_api.py JS
3. Re-dogfood
4. Assess Phase 3 vs diminishing returns
5. If diminishing returns justified, STOP and document