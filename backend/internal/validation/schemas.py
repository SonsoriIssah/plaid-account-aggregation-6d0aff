"""Pydantic request models — validation lives at the boundary so handlers trust their inputs."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateLinkRequest(BaseModel):
    institution_slug: str = Field(min_length=1, max_length=64)
