#!/usr/bin/env python3
"""Simulate OAuth2 credential collection and a protected tool call (offline)."""

from __future__ import annotations

from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, OAuth2Auth
from google.adk.auth.auth_schemes import AuthSchemeType, OpenIdConnectWithConfig
from google.adk.auth.auth_tool import AuthConfig
from google.adk.auth.credential_service.in_memory_credential_service import (
    InMemoryCredentialService,
)


def build_auth_config() -> AuthConfig:
    """Create a teaching AuthConfig resembling OAuth2/OIDC client setup."""
    # Scheme: OpenID Connect style endpoints (fake URLs for simulation).
    scheme = OpenIdConnectWithConfig(
        type_=AuthSchemeType.openIdConnect,
        authorization_endpoint="https://example-idp.local/oauth/authorize",
        token_endpoint="https://example-idp.local/oauth/token",
        scopes=["openid", "email", "profile"],
    )
    raw = AuthCredential(
        auth_type=AuthCredentialTypes.OPEN_ID_CONNECT,
        oauth2=OAuth2Auth(
            client_id="demo-client-id",
            client_secret="demo-client-secret",
        ),
    )
    return AuthConfig(
        auth_scheme=scheme,
        raw_auth_credential=raw,
        credential_key="demo_user_oidc",
    )


def simulate_user_consent(config: AuthConfig) -> AuthConfig:
    """Pretend the user finished the browser flow and tokens were exchanged."""
    exchanged = AuthCredential(
        auth_type=AuthCredentialTypes.OPEN_ID_CONNECT,
        oauth2=OAuth2Auth(
            client_id=config.raw_auth_credential.oauth2.client_id,
            client_secret=config.raw_auth_credential.oauth2.client_secret,
            access_token="ya29.simulated-access-token",
            refresh_token="1//simulated-refresh-token",
        ),
    )
    config.exchanged_auth_credential = exchanged
    return config


async def store_and_load(config: AuthConfig) -> None:
    from google.adk.auth.auth_credential import AuthCredential

    svc = InMemoryCredentialService()
    # Minimal save/load depending on API — print credential key contract.
    key = config.credential_key
    print("credential_key:", key)
    print("scheme type:", config.auth_scheme.type_)
    print(
        "after consent access_token prefix:",
        (config.exchanged_auth_credential.oauth2.access_token or "")[:12] + "…",
    )

    # Tool-side check pattern
    token = config.exchanged_auth_credential.oauth2.access_token
    if not token:
        raise SystemExit("No access token — tool must not call API")
    print("PROTECTED API CALL authorized with token fingerprint", token[:8] + "…")
    print("OK — simulated OAuth consent + tool authorization path")


def main() -> None:
    cfg = build_auth_config()
    print("STEP 1: tool requests credentials → AuthConfig created")
    print("  authorize URL would be:", cfg.auth_scheme.authorization_endpoint)

    print("STEP 2: client opens browser (simulated)")
    cfg = simulate_user_consent(cfg)

    print("STEP 3: store exchanged credential & call tool")
    import asyncio

    asyncio.run(store_and_load(cfg))


if __name__ == "__main__":
    main()
