# API

`GET /api/health` checks service availability. Create a journey with `POST /api/cases`, then use `POST /api/cases/{id}/story`, `/documents`, `/clarifications`, `/precautions-reviewed`, `/prepare-review`, `/follow-up`, `/complete`, and `/reopen`. Read state with `GET /api/cases/{id}`, `/documents/guidance`, and `/next-step`. `POST /api/assistant` supplies neutral contextual explanations.

Uploaded metadata accepts PDF, JPEG, PNG, and plain text only, with a 10 MB maximum. Uploaded files are never executed.
