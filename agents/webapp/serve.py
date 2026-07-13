#!/usr/bin/env python3
"""Serve the ADK course learning webapp (static files from public/)."""

from __future__ import annotations

import argparse
import functools
import http.server
import os
import socketserver
import sys
import webbrowser
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent / "public"
DEFAULT_PORT = 8765


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def end_headers(self) -> None:
        # Avoid stale course-data during local content rebuilds
        if self.path.endswith(".json") or self.path.endswith(".js"):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve ADK course webapp")
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-open", action="store_true", help="Do not open browser")
    parser.add_argument(
        "--build",
        action="store_true",
        help="Run scripts/build_content.py before serving",
    )
    args = parser.parse_args()

    if args.build:
        build = Path(__file__).resolve().parent / "scripts" / "build_content.py"
        import subprocess

        subprocess.check_call([sys.executable, str(build)])

    if not (PUBLIC / "index.html").is_file():
        print(f"Missing {PUBLIC / 'index.html'}", file=sys.stderr)
        sys.exit(1)
    if not (PUBLIC / "course-data.json").is_file():
        print(
            "Missing course-data.json — run: python scripts/build_content.py",
            file=sys.stderr,
        )
        sys.exit(1)

    os.chdir(PUBLIC)
    handler = functools.partial(QuietHandler, directory=str(PUBLIC))
    # Allow re-bind after restart
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", args.port), handler) as httpd:
        url = f"http://127.0.0.1:{args.port}/"
        print(f"ADK course webapp → {url}")
        print("  Ctrl+C to stop")
        if not args.no_open:
            try:
                webbrowser.open(url)
            except Exception:
                pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
