# Module 00 — Environment & ADK Setup

**Time:** 1–2 hours · **Difficulty:** Beginner

## Objectives

By the end of this module you will:

- Install Python 3.10+ and create a virtual environment
- Install Google ADK (`google-adk`)
- Create a Gemini API key and load it via `.env`
- Scaffold and run your first agent with ADK CLI

---

## 1. Prerequisites checklist

| Requirement | Check |
|-------------|--------|
| Python 3.10+ | `python3 --version` |
| pip | `pip --version` |
| Terminal / IDE | VS Code, Cursor, PyCharm, etc. |
| Internet | To call Gemini API |

---

## 2. Virtual environment

From the course root (`agents/`):

```bash
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows PowerShell
```

Upgrade pip (recommended):

```bash
pip install --upgrade pip
```

Install course dependencies:

```bash
pip install -r requirements.txt
```

Verify ADK CLI:

```bash
adk --help
```

You should see subcommands like `create`, `run`, `web`, `eval`.

---

## 3. API key (Gemini / Google AI Studio)

1. Open [Google AI Studio — API Keys](https://aistudio.google.com/app/apikey)
2. Create an API key
3. From the course root:

```bash
cp .env.example .env
```

4. Edit `.env`:

```bash
GOOGLE_API_KEY=paste_your_key_here
ADK_MODEL=gemini-flash-latest
```

**Security rules**

- Never commit `.env` or paste keys into chat/issues
- Prefer environment variables over hardcoding
- Rotate keys if exposed

### Optional: Vertex AI

For enterprise / GCP later:

```bash
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=your-project
export GOOGLE_CLOUD_LOCATION=us-central1
gcloud auth application-default login
```

Labs default to **AI Studio + API key**.

---

## 4. Project shape ADK expects

A minimal agent package:

```
my_agent/
├── __init__.py      # usually: from . import agent
├── agent.py         # defines root_agent
└── .env             # optional local env
```

ADK looks for a module with a **`root_agent`** object.

`agent.py` skeleton:

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-flash-latest",
    name="root_agent",
    description="A helpful assistant.",
    instruction="You are a concise, helpful assistant.",
)
```

---

## 5. Scaffold with CLI (optional)

You can scaffold anywhere:

```bash
adk create hello_adk
```

Answer prompts if asked, then:

```bash
# put key in hello_adk/.env or export GOOGLE_API_KEY
adk run hello_adk
```

---

## 6. Lab — Verify setup with course agent

This module includes a tiny **setup probe** agent.

```bash
# from course root, with venv active
export $(grep -v '^#' .env | xargs)   # loads .env into shell (macOS/Linux)

adk run modules/00-setup/setup_probe
```

**Try:**

```
Say hello and confirm you are online.
What is 2 + 2?
```

### Dev UI

```bash
adk web modules/00-setup --port 8000
```

Open `http://localhost:8000`, select `setup_probe`, chat.

> **Note:** ADK Web is for **development only**, not production.

---

## 7. Common setup failures

| Symptom | Fix |
|---------|-----|
| `adk: command not found` | Activate venv; `pip install google-adk` |
| Auth / 401 / API key errors | Check `GOOGLE_API_KEY` in env |
| Import errors | Python version; reinstall requirements |
| Agent not listed in `adk web` | Run web from parent dir of package folders |
| Model not found | Use `gemini-flash-latest` or a model your key can access |

---

## Checkpoint

1. What file must define `root_agent` for `adk run`?
2. Why use a virtual environment?
3. Is `adk web` safe for production? Why or why not?
4. Where do you get a free Gemini API key for learning?

**Answers (fold mental note):** (1) `agent.py` in the agent package (2) isolate deps (3) No — dev/debug only (4) Google AI Studio

---

## Next

→ [Module 01 — Agentic AI Foundations](../01-foundations/README.md)
