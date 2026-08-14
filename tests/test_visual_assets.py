from pathlib import Path
from xml.etree import ElementTree

from ai_governance_copilot_agent.generator import ROOT


VISUALS = ROOT / "assets" / "visuals"
EXPECTED_SVGS = {
    "authority-boundaries.svg",
    "guided-intake-loop.svg",
    "implementation-patterns.svg",
    "track-a-build-workflow.svg",
}


def test_svg_set_is_accessible_and_well_formed():
    actual = {path.name for path in VISUALS.glob("*.svg")}
    assert actual == EXPECTED_SVGS
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    for path in VISUALS.glob("*.svg"):
        root = ElementTree.parse(path).getroot()
        assert root.attrib["role"] == "img"
        assert root.attrib["aria-labelledby"] == "title desc"
        assert root.attrib.get("viewBox")
        title = root.find("svg:title", namespace)
        description = root.find("svg:desc", namespace)
        assert title is not None and title.text
        assert description is not None and description.text


def test_editable_mermaid_sources_cover_workflows():
    sources = VISUALS / "source"
    assert (sources / "authority-boundaries.mmd").exists()
    assert (sources / "guided-intake-loop.mmd").exists()
    assert (sources / "track-a-build-workflow.mmd").exists()
