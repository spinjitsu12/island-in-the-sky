# Asset catalog

## Stage 1 inventory

This stage contains one original reusable technical art asset. It calibrates the Blender-to-Godot pipeline, scale, named mesh parts, materials, and a lit inspection scene. It is not the final sanctuary environment or a claim of finished visual fidelity.

| Asset | Source | Runtime export | Status |
| --- | --- | --- | --- |
| `island_calibration` | `assets/source/blender/island_calibration.blend` | `assets/models/terrain/island_calibration.glb` | Generated and exported with Blender 5.2.2 LTS; integration checks recorded in `DEVELOPMENT.md` |

The adjacent `island_calibration.asset.json` is a machine-readable manifest containing mesh statistics, Godot-space bounds, all 160 perimeter positions, material names, provenance, generation version, and the current GLB SHA-256. Regeneration updates it automatically. Use that manifest for exact values; do not maintain a second binary hash here.

## Calibration island contract

- Parent: `island_calibration`; mesh children: `Surface` and `RockShell`.
- Scale: meters, with identity object translation/rotation/scale. The origin is the center of the footprint at reference elevation zero. The top gently rises above it; the suspended mass extends below it.
- Export conversion: the official Blender glTF exporter converts source +Z up to Godot +Y up, using `(x, y, z)` → `(x, z, -y)`. Do not apply a second axis rotation in Godot.
- Godot bounds: approximately 18.60 m wide × 8.60 m tall × 14.06 m deep; elevation ranges from −7.80 m to +0.804 m.
- Top: 24 radial rings with 160 samples each, gently rolling relief, and a broad inhabitable silhouette.
- Rock: 48 rings with 160 samples each, an offset tapered suspended mass, sculpted shoulders, vertical ribs, and selected unequal strata.
- Shared perimeter: all 160 top rim positions match the rock rim. Both parts deliberately have an open shared edge; together they enclose the island. They are separately reusable and replaceable mesh parts.
- Source counts: `Surface` has 3,841 vertices / 7,520 triangles; `RockShell` has 7,681 vertices / 15,200 triangles. Total: 11,522 source vertices / 22,720 triangles. glTF material boundaries can duplicate vertices during export/import.
- Surface data: perimeter positions are exported independently in the manifest. Later terrain chunks must maintain their own editable data and rebuildable mesh contract. This calibration mesh does not implement terrain expansion or sculpting.

## Materials

All materials use the Principled BSDF with zero metallic response and intentionally restrained roughness. The exporter transfers them as lit glTF PBR materials. No baked lighting, hidden image dependency, or unlit backdrop is used.

| Named material | Intended role | Roughness |
| --- | --- | --- |
| `Moss_Sage` | Main upper surface and rim contact band | 0.88 |
| `Moss_Light` | Broad, quieter surface variation | 0.88 |
| `Stone_Limestone` | Warm mineral body | 0.79 |
| `Stone_Ivory` | Selected pale mineral ribs | 0.75 |
| `Stone_CoolStrata` | Cool geological layers and underside | 0.84 |

The palette and forms are authored analytic geometry informed only by the moodboard's general themes. No models, textures, or distinctive designs from other games were copied. The thematic reference is private and is not distributed or used at runtime.

## Generation and quality gates

The asset generator is `tools/blender/build_calibration_asset.py`. Run it through Blender's background CLI, using `--factory-startup --python-exit-code 1 --python`, with `-- --project-root <project directory>` when the source directory is not the default. The script uses Blender's bundled Python only. It preserves the `.blend` source, exports a GLB through Blender's official exporter, and emits `CALIBRATION_ASSET_OK` on success.

Generation validates finite positions, mesh topology, and nondegenerate triangulation. Project foundation tests must also validate export integrity, material assignments, identity imported scale, meaningful bounds, and imported rim continuity. Headless import and a native GPU render are additional gates; current integrated results belong in `DEVELOPMENT.md` and limitations in `KNOWN_ISSUES.md`.

Reproducibility means identical generator/configuration with the same Blender/exporter version produces identical GLB content. The editable `.blend` container may carry Blender save metadata; byte identity of source files across sessions is not guaranteed. Verify the manifest's GLB hash after regeneration. Keep renderer captures and importer caches out of Git.

## Deliberate omissions and future asset families

The calibration island has no authored UVs, image textures, collision, LODs, vegetation, architecture, water, fauna, or animations. Material patches and smooth sculpted geometry are pipeline calibration, not final terrain material art. Planned work should add geological texture depth, production terrain edge treatments, foliage species, original open architecture, water features, and quiet sanctuary props as individually catalogued reusable assets after the foundation is accepted.
