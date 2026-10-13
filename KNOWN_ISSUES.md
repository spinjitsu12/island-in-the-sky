# Known issues and scope

- Stage 1 is an asset and pipeline study; it does not meet the final premium environment art bar.
- Material regions, geological forms, and procedural sky are calibration placeholders. Production UVs, texture detail, vegetation, water, architecture, weather, fauna, animation, and audio are future work.
- Terrain data seams are tested; runtime expansion, sculpting, mesh reconstruction, collision, persistence, and gameplay are not implemented.
- Native Forward+ is the validated renderer. Mobile/Compatibility parity, production performance budgets, and other platforms remain untested.
- Godot export templates are an external prerequisite for packaged builds. Packaged exports have not been validated.
- Direct `.blend` engine import is excluded; GLB is the interchange format.
- Blender 5.2 emits a `Material.use_nodes` deprecation notice concerning Blender 6; revalidate before upgrading major tool versions.
- Generated Blender save containers can change between sessions. Same-version GLB reproducibility was verified; cross-version binary identity is not promised.

No secrets, internal instructions, reference artwork, or machine-specific validation records are included in this public snapshot.
