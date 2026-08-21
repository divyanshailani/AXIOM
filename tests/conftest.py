import json
from pathlib import Path

import pytest

from axiom.bootstrap import MemoryBootstrap

BASE_DIR = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def loaded_memory() -> dict:
    """The patched memory dict exactly as the engine builds it at boot."""
    return MemoryBootstrap(BASE_DIR).load_memory()


@pytest.fixture(scope="session")
def router_config() -> Path:
    return BASE_DIR / "data" / "router_config.json"


@pytest.fixture(scope="session")
def retriever_config() -> Path:
    return BASE_DIR / "data" / "retriever_config.json"