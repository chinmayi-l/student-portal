# Student Portal

A responsive static student education management portal with three pages:

- `index.html` — Home
- `dashboard.html` — Student Dashboard
- `assistant.html` — AI Assistant chat

## Run the FastAPI backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

Serve the frontend from the same origin (or configure a reverse proxy) so the assistant can POST JSON messages to `/chat`.

```json
{ "message": "Help me create a study plan" }
```
