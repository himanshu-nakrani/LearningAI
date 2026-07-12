# Module 11 — Artifacts (files, blobs, versioning)

**Time:** 2–3 hours · **Docs:** [Artifacts](https://adk.dev/artifacts/)

## Objectives

- Explain when to use **artifacts** vs **state**
- Configure `InMemoryArtifactService` / `GcsArtifactService` on `Runner`
- Save/load versioned binary data via context
- Use session vs `user:` namespaces
- Reference artifacts in instructions (`{artifact.name?}`)

---

## 1. Why artifacts?

| Use state for | Use artifacts for |
|---------------|-------------------|
| Small JSON flags | PDFs, images, audio, CSV blobs |
| Counters, lists of strings | Multi-MB outputs |
| Cross-agent scratch fields | User uploads / generated reports |

Representation: `google.genai.types.Part` with `inline_data` (`Blob`: `data` + `mime_type`).

---

## 2. ArtifactService

```python
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner

runner = Runner(
    agent=agent,
    app_name="artifact_app",
    session_service=session_service,
    artifact_service=InMemoryArtifactService(),
)
```

Methods (service / context wrappers):

- `save_artifact(filename, artifact)` → version int  
- `load_artifact(filename, version=None)` → latest if None  
- `list_artifact_keys` / `list_versions` / `delete_artifact`  

**Namespaces:**

- `report.pdf` → session-scoped  
- `user:avatar.png` → user-scoped across sessions (GCS-backed services)

---

## 3. Lab

```bash
python modules/11-artifacts/run_artifact_demo.py
adk run modules/11-artifacts/artifact_demo   # instruction-level awareness
```

### Exercises

1. Save both a session report and `user:profile.txt`.  
2. Load version 0 explicitly after saving twice.  
3. Sketch GCS bucket IAM for production.  

---

## Checkpoint

1. Why is MIME type required?  
2. What does save return?  
3. When would GCS beat InMemory?  

## Next

→ [Module 12 — Callbacks & Plugins](../12-callbacks-plugins/README.md)
