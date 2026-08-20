"""Institutions are configured connectors. For the MVP they live in code,
but the registry interface is what a future DB-backed catalog would implement."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InstitutionConfig:
    slug: str
    name: str
    oauth_authorize_url: str


_INSTITUTIONS: dict[str, InstitutionConfig] = {
    "mockbank": InstitutionConfig(
        slug="mockbank",
        name="MockBank Sandbox",
        oauth_authorize_url="https://mockbank.local/oauth/authorize",
    ),
}


def list_institutions() -> list[InstitutionConfig]:
    return list(_INSTITUTIONS.values())


def get_institution(slug: str) -> InstitutionConfig | None:
    return _INSTITUTIONS.get(slug)
