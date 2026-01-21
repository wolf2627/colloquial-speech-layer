"""
Dynamic Endpoint Router.
Auto-discovers modules in /src and creates POST endpoints for each.
"""

import importlib
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import config

router = APIRouter()


class RequestPayload(BaseModel):
    """Standard request payload for all endpoints."""
    input: str


class ResponsePayload(BaseModel):
    """Standard response payload for all endpoints."""
    output: str
    endpoint: str


def discover_modules() -> list[str]:
    """Discover all handler modules in /src directory."""
    modules = []
    src_dir = config.SRC_DIR
    
    if not src_dir.exists():
        return modules
    
    for file in src_dir.glob("*.py"):
        # Skip __init__ and base_model
        if file.name.startswith("_") or file.name == "base_model.py":
            continue
        module_name = file.stem
        modules.append(module_name)
    
    return modules


def get_process_function(module_name: str):
    """Get the process function from a module."""
    try:
        module = importlib.import_module(f"src.{module_name}")
        
        if hasattr(module, 'process'):
            return module.process
        
        raise ValueError(f"No process() function found in {module_name}")
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Failed to load module: {e}")


@router.get("/models")
async def list_models() -> dict[str, Any]:
    """List all available model endpoints."""
    modules = discover_modules()
    return {
        "models": modules,
        "count": len(modules)
    }


@router.post("/{endpoint}")
async def process_request(endpoint: str, payload: RequestPayload) -> ResponsePayload:
    """
    Dynamic endpoint handler.
    Routes requests to the appropriate module's process() function.
    """
    modules = discover_modules()
    
    if endpoint not in modules:
        raise HTTPException(
            status_code=404,
            detail=f"Endpoint '{endpoint}' not found. Available: {modules}"
        )
    
    try:
        process_fn = get_process_function(endpoint)
        
        # Call the process function with just the input
        result = process_fn(user_input=payload.input)
        
        return ResponsePayload(
            output=result,
            endpoint=endpoint
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
