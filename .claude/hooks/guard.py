"""PreToolUse guard hook. Copy to .claude/hooks/guard.py in a repo.

Claude Code sends the pending tool call as JSON on stdin. Exit code 2 blocks the
call and sends the message on stderr back to Claude; exit code 0 allows it.
Fails closed: if the input can't be read, the call is blocked.
"""
import json
import sys

PROTECTED_DIRS = ("reference/",)          # originals: never edited
BLOCKED_COMMANDS = (
    "git push origin main",
    "git push --force",
    "git push -f",
    "git reset --hard",
)


def block(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(2)


try:
    data = json.load(sys.stdin)
except Exception:
    block("guard.py could not read the tool call; blocked to be safe.")

tool = data.get("tool_name", "")
tool_input = data.get("tool_input", {}) or {}

if tool in ("Edit", "Write"):
    path = str(tool_input.get("file_path", "")).replace("\\", "/")
    if any(f"/{d}" in "/" + path for d in PROTECTED_DIRS):
        block(f"{path} is in a read-only originals folder. Make a copy elsewhere instead.")

if tool == "Bash":
    cmd = " ".join(str(tool_input.get("command", "")).split())
    for bad in BLOCKED_COMMANDS:
        if bad in cmd:
            block(f"'{bad}' is not allowed here. Use a branch and open a pull request.")

sys.exit(0)
