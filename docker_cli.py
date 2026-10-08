import asyncio
import subprocess

DOCKER_TIMEOUT = 60


def run_docker(*args: str) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            ["docker", *args],
            capture_output=True,
            text=True,
            check=False,
            timeout=DOCKER_TIMEOUT,
        )
    except FileNotFoundError:
        return 127, "docker not found in PATH"
    except subprocess.TimeoutExpired:
        return 124, f"Timeout: docker {' '.join(args)} took too long"
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


async def docker(*args: str) -> tuple[int, str]:
    return await asyncio.to_thread(run_docker, *args)
