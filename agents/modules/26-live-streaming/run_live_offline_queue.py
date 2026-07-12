#!/usr/bin/env python3
"""Offline smoke: LiveRequestQueue API (no model call)."""

from __future__ import annotations

import asyncio

from google.adk.agents.live_request_queue import LiveRequestQueue
from google.genai import types


async def main() -> None:
    q = LiveRequestQueue()
    q.send_content(
        types.Content(role="user", parts=[types.Part(text="hello live")])
    )
    q.send_activity_start()
    q.send_activity_end()
    q.close()

    print("Draining LiveRequestQueue:")
    while True:
        req = await q.get()
        print(" ", req)
        if getattr(req, "close", False):
            break
    print("OK — queue protocol works")


if __name__ == "__main__":
    asyncio.run(main())
