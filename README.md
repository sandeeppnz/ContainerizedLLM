# Streamlit LLM Chat (Docker-First, OpenAI-Compatible)

A minimal Streamlit chat UI that talks to **any OpenAI-compatible Chat Completions API** (local LLM servers such as llama.cpp/Ollama proxies or hosted providers).  
This project is **Docker-first** — you build and run the app in a container with a simple `.env` file for configuration.

<img width="864" height="641" alt="image" src="https://github.com/user-attachments/assets/e5035366-2049-40e4-929a-0b9b09121eb8" />

---

## Why Docker?

- ✅ **Reproducible**: same environment for everyone
- 🔐 **Isolated**: no Python deps leaking into your machine
- ⚙️ **Config via `.env`**: swap endpoints/models without code changes
- 🖥️ **Local-friendly**: easily point to a local or remote LLM server

---

## Quick Start (Docker)

### 1) Prepare `.env`
Create a file named `.env` in the project root. Choose either a local server or OpenAI:

**Local server (example: llama.cpp/Ollama proxy)**
```env
BASE_URL=http://host.docker.internal:12434/engines/llama.cpp/v1/
API_KEY=anything
MODEL=llama3.2
```

**OpenAI (official)**
```env
BASE_URL=https://api.openai.com/v1/
API_KEY=sk-...your_key...
MODEL=gpt-4o-mini
```

> On Linux, `host.docker.internal` may not resolve by default. Start the container with:  
> `--add-host=host.docker.internal:host-gateway`

### 2) Build
```bash
docker build -t streamlit-llm-chat .
```

### 3) Run
```bash
docker run --rm \
  -p 8501:8501 \
  --env-file .env \
  --add-host=host.docker.internal:host-gateway \
  streamlit-llm-chat
```
Open **http://localhost:8501** and chat away.

---

## Docker Compose (optional)

Create a `docker-compose.yml`:
```yaml
services:
  app:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
    extra_hosts:
      - "host.docker.internal:host-gateway"  # helpful for Linux
```
Then:
```bash
docker compose up --build
```

---

## Environment Variables

- `BASE_URL` — Chat Completions base URL (must end with `/v1/` for most servers)
- `API_KEY` — API key (placeholder is fine for many local servers)
- `MODEL` — Model name (e.g., `llama3.2`, `gpt-4o-mini`)

> The app reads these at runtime; no code edits required.

---

## Architecture (at a glance)

- **Streamlit** serves the UI from inside a container.
- The app calls your configured **OpenAI-compatible** endpoint for chat responses.

---

## Troubleshooting

- **Cannot reach local LLM server from container**  
  Use `host.docker.internal` in `BASE_URL` and add `--add-host=host.docker.internal:host-gateway` on Linux.
- **401/403**  
  Check `API_KEY` and that your provider allows the selected model.
- **404/405**  
  Verify that `BASE_URL` is correct and typically ends with `/v1/`.
- **Blank response**  
  Some servers return different shapes; check container logs: `docker logs <container>`.

---

## Security Notes

- Treat `.env` as sensitive if it contains real keys (add to `.gitignore`).
- Prefer HTTPS for remote endpoints (`BASE_URL=https://...`).

---

## License

MIT
