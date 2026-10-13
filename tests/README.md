# Foundation checks

Run `python3 tools/pipeline.py import`, then `python3 tools/pipeline.py test`.

`validate_asset.py` reads the exported GLB independently and verifies its container, manifest hash, preserved source, two-mesh contract, and material references. `foundation_test.gd` loads the actual imported scene, checks materials, scale, axis conversion, and all shared rim samples. It also checks positive/negative chunk neighbors, independent sample storage, rejection of malformed/nonfinite data, and camera distance/pitch limits.

Run `python3 tools/pipeline.py render` for native Forward+ shader and scene validation. Inspect the resulting image: existence alone does not prove acceptable composition. Tests do not establish final art quality or target-device performance. The static calibration GLB and terrain lattice are deliberately independent until a later mesh adapter milestone.
