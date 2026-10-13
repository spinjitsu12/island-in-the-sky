# Floating Island Sanctuary

An original, peaceful 3D sanctuary above a sea of clouds, by [spinjitsu12](https://github.com/spinjitsu12).

**Copyright © 2026 spinjitsu12. All rights reserved. Express written permission is required for reuse. This is not an open-source project.** See [LICENSE](LICENSE) and [CONTRIBUTING.md](CONTRIBUTING.md). Public visibility and GitHub forks do not grant additional reuse permission beyond GitHub's terms and applicable law.

## Current milestone

Stage 1 establishes the Blender → GLB → Godot pipeline: a reusable calibration island, lit 3D inspection scene, eased orbit camera, and a terrain height/boundary data contract. This is a technical foundation, not the finished environment or a playable game. Premium environment art, landscape building, water, vegetation, architecture, wildlife, and terrain editing are future stages.

The long-term visual direction is detailed, original anime-inspired 3D scenery with cinematic lighting, refined natural forms, and calm interaction. The reference artwork and internal development records are private; neither is needed to run this project.

## Technical review

The foundation has passed source generation, reproducible GLB export, fresh-cache engine import, 30 automated foundation checks, and native Forward+ screenshot review at three angles. Read [DEVELOPMENT.md](DEVELOPMENT.md) and [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for scope and limitations.

For parties with permission to run or modify the project, the supported baseline is Godot 4.7.2, Blender 5.2.2 LTS, and Python 3.9 or newer. Open `project.godot` in Godot. Review controls: drag to orbit, scroll to zoom, and R to reset.

```sh
python3 tools/pipeline.py build
python3 tools/pipeline.py import
python3 tools/pipeline.py test
python3 tools/pipeline.py render
```

`all` runs that sequence. `render --view reverse` and `render --view top` capture other review angles. Native rendering requires a graphical session. The runner discovers Blender/Godot on PATH or in standard macOS locations; `BLENDER_BIN` and `GODOT_BIN` can override discovery.

## Source layout

| Directory | Purpose |
| --- | --- |
| `assets/source/blender` | Editable Blender source, with private filename metadata removed |
| `assets/models` | Runtime GLB and asset manifests |
| `assets/textures`, `assets/materials`, `assets/shaders` | Visual resources |
| `assets/animations`, `assets/effects` | Animation/effects resources |
| `scripts`, `scenes`, `ui` | GDScript, scenes, inspection interface |
| `tools`, `tests` | Rebuild pipeline and integrity checks |
| `docs` | Technical architecture |

[ART_DIRECTION.md](ART_DIRECTION.md), [ASSET_CATALOG.md](ASSET_CATALOG.md), and [ROADMAP.md](ROADMAP.md) describe the project's standards and staged goals. External tool licensing is documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
