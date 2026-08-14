from pathlib import Path
import re

from ai_governance_copilot_agent.generator import ROOT


TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".toml"}


def test_repository_contains_no_known_private_organization_names():
    prohibited = ("marketaxess",)
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        content = path.read_text(errors="ignore").lower()
        for value in prohibited:
            assert value not in content, f"private organization name found in {path}"


def test_relative_markdown_links_resolve():
    link_pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        for target in link_pattern.findall(path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            assert resolved.exists(), f"broken link in {path}: {target}"
