# Module 26 — Live Streaming & Bidirectional Mode

**Time:** 2–3 hours · **APIs:** `Runner.run_live`, `LiveRequestQueue`, `RunConfig`, `StreamingMode`

## Objectives

- Contrast turn-based `run_async` vs live bidirectional streaming  
- Configure `RunConfig` (SSE vs BIDI, modalities, session resumption)  
- Drive a live session with `LiveRequestQueue`  
- Know when mic/audio is required vs text-only streaming  

---

## 1. Two streaming modes

| Mode | API | Use |
|------|-----|-----|
| **SSE** | `run_async(..., run_config=RunConfig(streaming_mode=StreamingMode.SSE))` | Partial text tokens as they generate |
| **BIDI / Live** | `run_live(live_request_queue=..., run_config=...)` | Continuous duplex (voice/video + tools) |

```python
from google.adk.agents.live_request_queue import LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode

queue = LiveRequestQueue()
queue.send_content(types.Content(role="user", parts=[types.Part(text="Hello")]))
# later: queue.close()

async for event in runner.run_live(
    user_id="u",
    session_id="s",
    live_request_queue=queue,
    run_config=RunConfig(streaming_mode=StreamingMode.BIDI),
):
    ...
```

---

## 2. Labs in this module

| Script | Needs API key? | What it does |
|--------|----------------|--------------|
| `run_sse_stream.py` | Yes | Token streaming via SSE |
| `run_live_text_session.py` | Yes | Live queue with text turns |
| `run_live_offline_queue.py` | No | Queue API smoke without model |

```bash
python modules/26-live-streaming/run_live_offline_queue.py
# with key:
python modules/26-live-streaming/run_sse_stream.py
python modules/26-live-streaming/run_live_text_session.py
```

---

## 3. Production notes

- Prefer **short tools** on the live path (latency)  
- Handle partials vs final transcripts  
- Consent/recording if saving audio blobs (`save_live_blob`)  
- Fallback to turn-based chat if live websocket fails  

## Checkpoint

1. SSE vs BIDI difference?  
2. What closes a live session from the client side?  

## Next

→ [Module 27 — OAuth flow](../27-oauth-flow/README.md)
