import asyncio
import functools
import socket
import subprocess
from pathlib import Path

from config import PROTECTED_CONTAINERS
from docker_cli import docker


def _inside_container() -> bool:
    return Path("/.dockerenv").exists()


@functools.lru_cache(maxsize=1)
def self_container_name() -> str | None:
    if not _inside_container():
        return None
    cid = socket.gethostname()[:12]
    try:
        proc = subprocess.run(
            ["docker", "ps", "--filter", f"id={cid}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    name = proc.stdout.strip()
    return name or None


def protected_names() -> frozenset[str]:
    names = set(PROTECTED_CONTAINERS)
    own = self_container_name()
    if own:
        names.add(own)
    return frozenset(names)


def list_protected() -> list[str]:
    return sorted(protected_names())


async def resolve_name(name: str) -> str:
    _, out = await docker("ps", "-a", "--format", "{{.Names}}")
    existing = [line.strip() for line in out.splitlines() if line.strip()]
    if name in existing:
        return name
    matches = [n for n in existing if n.startswith(name)]
    return matches[0] if len(matches) == 1 else name


async def is_protected(name: str) -> bool:
    protected = protected_names()
    if not protected:
        return False
    target = await resolve_name(name)
    return any(target == p or p.startswith(target) for p in protected)


def _compose_names_sync(path: Path) -> list[str]:
    try:
        proc = subprocess.run(
            ["docker", "compose", "ps", "-a", "--format", "{{.Name}}"],
            cwd=str(path),
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


async def compose_conflict(path: Path) -> str | None:
    protected = protected_names()
    if not protected:
        return None
    names = await asyncio.to_thread(_compose_names_sync, path)
    for name in names:
        if any(name == p or p.startswith(name) for p in protected):
            return name
    return None
