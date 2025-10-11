"""Health endpoint for the SWAT-Copilot API."""
from fastapi import APIRouter

router = APIRouter(prefix="/healthz", tags=["health"])


@router.get("", summary="Check API health")
def health() -> dict[str, bool]:
    return {"ok": True}
