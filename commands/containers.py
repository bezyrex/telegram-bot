from telegram import Update
from telegram.ext import ContextTypes

from docker_cli import docker
from helpers import refuse_protected, reply, usage
from protection import list_protected


def container_op(command: str, *extra: str, usage_name: str | None = None):
    shown = usage_name or command

    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args:
            await usage(update, f"Usage: /{shown} <name>")
            return
        name = context.args[0]
        if await refuse_protected(update, name):
            return
        code, out = await docker(command, *extra, name)
        await reply(update, out or f"docker {command} failed (code {code})")

    handler.__name__ = f"cmd_{shown}"
    return handler


async def cmd_ps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = ["ps", "-a"]
    if context.args:
        args += ["--filter", f"name={context.args[0]}"]
    args += ["--format", "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"]
    code, out = await docker(*args)
    await reply(update, out or f"docker ps failed (code {code})")


async def cmd_inspect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await usage(update, "Usage: /inspect <name>")
        return
    code, out = await docker("inspect", context.args[0])
    await reply(update, out or f"docker inspect failed (code {code})")


async def cmd_logs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await usage(update, "Usage: /logs <name> [lines]")
        return
    name = context.args[0]
    lines = (
        context.args[1]
        if len(context.args) > 1 and context.args[1].isdigit()
        else "50"
    )
    code, out = await docker("logs", "--tail", lines, name)
    await reply(update, out or f"docker logs failed (code {code})")


async def cmd_exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await usage(update, "Usage: /exec <name> <command>")
        return
    name, *parts = context.args
    code, out = await docker("exec", name, "sh", "-c", " ".join(parts))
    await reply(update, out or f"exec returned code {code}")


async def cmd_top(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await usage(update, "Usage: /top <name>")
        return
    code, out = await docker("top", context.args[0])
    await reply(update, out or f"docker top failed (code {code})")


async def cmd_protected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    names = list_protected()
    await reply(update, "\n".join(names) or "No protected containers.")


HANDLERS = [
    ("ps", cmd_ps),
    ("psa", cmd_ps),
    ("inspect", cmd_inspect),
    ("logs", cmd_logs),
    ("stop", container_op("stop")),
    ("start_c", container_op("start", usage_name="start_c")),
    ("restart", container_op("restart")),
    ("rm", container_op("rm", "-f")),
    ("exec", cmd_exec),
    ("top", cmd_top),
    ("protected", cmd_protected),
]
