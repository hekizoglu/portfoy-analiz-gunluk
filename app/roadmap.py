from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(slots=True)
class RoadmapTask:
    task_id: str
    title: str
    phase: str
    status: str


TASK_BLOCK_RE = re.compile(
    r"### Task (?P<id>[A-Z0-9\-]+)\n"
    r"- ID: `(?P=id)`\n"
    r"- Title: `?(?P<title>.+?)`?\n"
    r"- Phase: `(?P<phase>.+?)`\n"
    r"- Status: `(?P<status>.+?)`",
    re.MULTILINE,
)


def find_next_todo_task(path: Path) -> RoadmapTask | None:
    text = path.read_text(encoding="utf-8")
    for match in TASK_BLOCK_RE.finditer(text):
        status = match.group("status").strip()
        if status == "TODO":
            return RoadmapTask(
                task_id=match.group("id").strip(),
                title=match.group("title").strip(),
                phase=match.group("phase").strip(),
                status=status,
            )
    return None
