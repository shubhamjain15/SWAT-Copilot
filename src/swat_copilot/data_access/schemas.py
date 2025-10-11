"""Pydantic models describing persisted SWAT structures."""
from pydantic import BaseModel


class SUBRecord(BaseModel):
    """Lightweight representation of a SUB table row."""

    sub: int
    area_km2: float
