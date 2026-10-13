# Development

All use requires permission as set out in [LICENSE](LICENSE). This document describes the technical pipeline for authorized work.

## Toolchain and commands

Validated baseline: Godot 4.7.2 stable, Blender 5.2.2 LTS with its bundled Python API, Python 3.9+, and Git. No third-party Python packages are required.

Run from the project root:

```sh
python3 tools/pipeline.py build
python3 tools/pipeline.py import
python3 tools/pipeline.py test
python3 tools/pipeline.py render
```

`build` writes the editable Blender source, runtime GLB, and manifest. `import` creates Godot's disposable cache. `test` checks container/hash/source integrity, imported mesh/material/scale/rim contracts, chunk neighbor consistency, and camera bounds/easing. `render` saves a native Forward+ image to `build/validation/foundation.png`; inspect it visually. `all` runs the sequence. Use `render --view reverse` or `render --view top` for additional angles.

The runner searches PATH and standard macOS application directories. Set `BLENDER_BIN` or `GODOT_BIN` for other executable locations. Native rendering uses Metal on macOS and Vulkan elsewhere; other platforms remain unvalidated. Logs, captures, and `.godot` caches are ignored. Sandbox restrictions can require permission to launch external applications; do not treat a headless run as GPU validation.

## Asset contract

Work in meters. Blender uses +Z up; glTF converts to Godot +Y up. Keep stable object/material names, identity mesh transforms, intentional origins, and preserved editable sources. Full-precision imports and disabled automatic LOD generation preserve this calibration asset's shared rim. Production compression/LOD policy needs separate validation.

`TerrainChunkData` stores an inclusive lattice and world-space boundary convention independently of render meshes. The calibration GLB is not yet generated from this data. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Future mesh reconstruction, sculpting, persistence, collision, and expansion require dedicated implementation and tests.

## Review gates

Validate generator changes through export, fresh import, integrity tests, and native visual review. Update the catalog/changelog/issues with actual results. Keep private notes, credentials, local paths, reference artwork, agent instructions, and personal metadata out of repository contents and history. The project license does not override licenses on third-party components.
