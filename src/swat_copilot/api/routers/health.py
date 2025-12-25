"""Health check endpoints."""

from fastapi import APIRouter

from swat_copilot import __version__

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "version": __version__,
    }


@router.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns:
        Welcome message
    """
    return {
        "message": "SWAT-Copilot API",
        "version": __version__,
        "docs": "/docs",
    }
