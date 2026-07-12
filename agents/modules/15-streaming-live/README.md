# Module 15 — Streaming, Gemini Live & Multimodal

**Time:** 2–3 hours · **Docs:** [Streaming / Live toolkit](https://adk.dev/streaming/)

## Objectives

- Distinguish turn-based `run` / `run_async` from **live bidirectional** sessions  
- Know `run_live()` and **RunConfig** knobs  
- Plan voice/video agent architectures  
- Apply safety and latency considerations  

---

## 1. Two interaction modes

| Mode | API style | UX |
|------|-----------|-----|
| Turn-based | `runner.run` / `run_async` | Chat messages, tool calls between turns |
| Live | `run_live()` + Live API | Low-latency audio/video duplex |

ADK’s **Gemini Live API Toolkit** wraps Gemini Live for ADK agents (tools still work; multi-agent possible).

---

## 2. RunConfig themes (study checklist)

From Live toolkit parts:

- Response modalities (text / audio)  
- Streaming modes  
- Session management & resumption  
- Context window compression  
- Quota management  
- Automatic tool execution during live sessions  

Read: [Streaming dev guide](https://adk.dev/streaming/) parts 1–4 on adk.dev.

---

## 3. Streaming tools

Tools can stream intermediate results; agents can react mid-stream. Use for:

- Long scrapes  
- Progressive code execution  
- Partial search results  

---

## 4. Architecture sketch

```
Mic/Camera → Live session → ADK Agent (+ tools)
                │
                ├─ tool calls (async)
                └─ audio/text out
```

Production concerns:

- Interruptions / barge-in  
- VAD (voice activity)  
- Partial transcripts vs final  
- Tool latency vs conversational feel  
- Recording/consent compliance  

---

## 5. Lab (environment-dependent)

Live APIs typically need:

- Compatible Gemini model  
- Audio device / client  
- Correct auth  

**Exercises (no special hardware required):**

1. Write a product brief for a voice support agent using ADK Live.  
2. List which tools must be **fast** (<300ms) vs acceptable slow.  
3. Design a fallback: live fails → text chat with same `root_agent`.  
4. Trace how a tool call appears in live event stream (read docs Part 3).  

---

## Checkpoint

1. When is turn-based enough?  
2. Name two RunConfig concerns.  
3. Why can long tools break voice UX?  

## Next

→ [Module 16 — Models, Config, Runtime & Events](../16-models-config-runtime/README.md)
