# notes-app-code

Flask Notes API with a PostgreSQL database.
Deployment files (Kubernetes) are in the separate `notes-app-deployment` repo.

## Files
| File | Purpose |
|---|---|
| app.py | the application |
| db/init.sql | database table creation (runs when the app starts) |
| requirements.txt | Python packages |
| Dockerfile | recipe to build the image |

## Endpoints
- `GET /health`
- `GET /notes`
- `POST /notes` with JSON `{"text": "hello"}`

## Build and push an image (always use a version tag)
```bash
docker login
docker build -t <dockerhub-username>/notes-app:1.0 .
docker push <dockerhub-username>/notes-app:1.0
```

Next version: change the code, then build and push `1.1`, `1.2`, and so on.
Also mark the same version in Git:
```bash
git tag v1.0
git push origin v1.0
```
