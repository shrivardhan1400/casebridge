# Architecture

CaseBridge keeps the original premium browser prototype in `frontend/index.html` and provides a deployable FastAPI application for persistent integration.

```text
Frontend → API → Case service → Domain services
                              ├─ Prototype story extraction
                              ├─ Information checklist
                              ├─ Document guidance and safe upload metadata
                              ├─ Source mapping
                              ├─ Clarification engine
                              ├─ Timeline builder
                              ├─ Next-step engine
                              ├─ Human-review package
                              └─ Follow-up workflow
```

The local extractor is deterministic and intentionally labelled a prototype. Every field has an explicit provenance label. The API stores cases in memory for the hackathon prototype; production deployment should add authenticated encrypted persistence and object storage.
