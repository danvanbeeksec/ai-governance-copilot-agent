# Maintain generated derivatives

The committed files under `generated/` are derived from exact GitHub dependency pins. They make the kit usable without requiring practitioners to install Python.

Maintainers regenerate them with:

```bash
python -m pip install -r requirements-dev.txt
build-copilot-agent-assets
python -m pytest
```

The generator writes a manifest containing source provenance and a SHA-256 hash for every artifact. CI regenerates the assets and fails if the committed copies drift.

When updating a source:

1. review and merge the authoritative Framework or Control Plane change first;
2. update the exact dependency commit in `pyproject.toml` and `sources.lock.yaml`;
3. regenerate all derivatives;
4. inspect content and provenance changes;
5. run automated and conversational tests;
6. update the compatibility table and changelog; and
7. publish a reviewed kit release.

Never edit generated knowledge or decision specifications as an independent source of truth.
