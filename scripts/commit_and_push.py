from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", required=True)
    args = parser.parse_args()

    status = run_git("status", "--short")
    if not status.stdout.strip():
        print("GIT_STATUS=NO_CHANGES")
        return 0

    add = run_git("add", ".")
    if add.returncode != 0:
        print(add.stderr.strip(), file=sys.stderr)
        return add.returncode

    commit = run_git("commit", "-m", args.message)
    if commit.returncode != 0:
        print(commit.stderr.strip() or commit.stdout.strip(), file=sys.stderr)
        return commit.returncode

    remote = run_git("remote", "-v")
    if "origin" not in remote.stdout:
        print("PUSH_STATUS=SKIPPED_NO_REMOTE")
        return 0

    push = run_git("push")
    if push.returncode != 0:
        print(push.stderr.strip() or push.stdout.strip(), file=sys.stderr)
        return push.returncode

    print("PUSH_STATUS=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
