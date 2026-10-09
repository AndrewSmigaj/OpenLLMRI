#!/usr/bin/env python3
"""
The experiments health check. (The LLM insights and scaffold-step routes retired in lens slice 1:
the checked LLM analysis in api/routers/analysis.py replaced them.)
"""

from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/experiments/health")
async def health_check() -> Dict[str, str]:
    """Health check for experiments API."""
    return {"status": "healthy", "service": "expert_route_analysis"}
