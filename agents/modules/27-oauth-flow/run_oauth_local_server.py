#!/usr/bin/env python3
"""Optional real OAuth2 authorization-code server (Google or any OIDC).

Requires:
  OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
  Optional: OAUTH_AUTH_URL, OAUTH_TOKEN_URL, OAUTH_SCOPES

This is a teaching server — do not use in production.
"""

from __future__ import annotations

import os
import secrets
import sys
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer


CLIENT_ID = os.getenv("OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET", "")
AUTH_URL = os.getenv(
    "OAUTH_AUTH_URL", "https://accounts.google.com/o/oauth2/v2/auth"
)
TOKEN_URL = os.getenv("OAUTH_TOKEN_URL", "https://oauth2.googleapis.com/token")
SCOPES = os.getenv("OAUTH_SCOPES", "openid email profile")
REDIRECT = "http://127.0.0.1:8765/callback"
STATE = secrets.token_urlsafe(16)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            params = {
                "client_id": CLIENT_ID,
                "redirect_uri": REDIRECT,
                "response_type": "code",
                "scope": SCOPES,
                "state": STATE,
                "access_type": "offline",
                "prompt": "consent",
            }
            url = AUTH_URL + "?" + urllib.parse.urlencode(params)
            self.send_response(302)
            self.send_header("Location", url)
            self.end_headers()
            return
        if parsed.path == "/callback":
            qs = urllib.parse.parse_qs(parsed.query)
            if qs.get("state", [None])[0] != STATE:
                self._html(400, "Invalid state")
                return
            code = qs.get("code", [None])[0]
            if not code:
                self._html(400, f"Error: {qs}")
                return
            token = self._exchange(code)
            self._html(200, f"<pre>{token}</pre><p>Copy tokens into credential service.</p>")
            return
        self._html(404, "Not found")

    def _exchange(self, code: str) -> str:
        data = urllib.parse.urlencode(
            {
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT,
                "grant_type": "authorization_code",
            }
        ).encode()
        req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode()

    def _html(self, code: int, body: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, fmt: str, *args) -> None:  # quieter
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main() -> None:
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Set OAUTH_CLIENT_ID and OAUTH_CLIENT_SECRET")
        print("Or run offline: python modules/27-oauth-flow/run_oauth_simulation.py")
        sys.exit(1)
    print("Open http://127.0.0.1:8765/  (redirect URI must be registered)")
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()


if __name__ == "__main__":
    main()
