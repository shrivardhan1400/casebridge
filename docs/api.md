# API

`GET /api/health` checks service availability. Create a journey with `POST /api/cases`, then use `POST /api/cases/{id}/story`, `/documents`, `/clarifications`, `/precautions-reviewed`, `/prepare-review`, `/follow-up`, `/complete`, and `/reopen`. Read state with `GET /api/cases/{id}`, `/documents/guidance`, and `/next-step`. `POST /api/assistant` supplies neutral contextual explanations.

Uploaded metadata accepts PDF, JPEG, PNG, and plain text only, with a 10 MB maximum. Uploaded files are never executed.

Additional domain flows: `POST /api/demo/rental` generates the deterministic synthetic rental demo; `POST /api/notices/explain` organizes visible notice text without legal conclusions; `POST /api/cases/{id}/documents/analyze` runs prototype visible-text extraction; `GET /api/cases/{id}/source-map` returns provenance labels; `GET /api/cases/{id}/review-package` returns the current human-review package; and `POST /api/cases/{id}/follow-up/{follow_up_id}/complete` records user-controlled follow-up completion.
