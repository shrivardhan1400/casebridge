# Evaluator Alignment

The declared CaseBridge workflow is implemented as inspectable Python modules, not only as UI copy.

| Declared capability | Executable implementation |
| --- | --- |
| Situation classification and story intake | `LocalDemoExtractor.extract` |
| Dynamic missing information | `detect_missing_information` |
| Contextual document guidance | `recommend_documents` |
| Safe document analysis | `analyze_visible_text` |
| Source / provenance mapping | `map_document_fields`, `build_source_map` |
| Cross-source difference detection | `detect_amount_differences` |
| Timeline and human review package | `build_timeline`, `review_package` |
| State-based next step | `next_step` |
| Contextual assistant safety boundary | `contextual_answer` |
| Court Notice Explainer | `explain_court_notice` |
| Follow-up, completion, reopen | `mark_follow_up_complete`, `reopen_journey` |
| Deterministic rental demo | `create_rental_demo` |

## SDG 9: Industry, Innovation and Infrastructure

CaseBridge supports SDG 9 by demonstrating a modular, testable civic-tech information workflow. Its innovation is not an automated legal decision: it is a traceable information infrastructure that preserves provenance, exposes uncertainty, and prepares a structured package for a human reviewer. The local deterministic extractor provides reproducible prototype behavior and can be replaced by a governed provider later.
