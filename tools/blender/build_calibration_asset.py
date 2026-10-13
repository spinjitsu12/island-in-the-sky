# Copyright (c) 2026 spinjitsu12. All rights reserved.
# Express written permission required; see LICENSE.
"""Build an original, deterministic pipeline calibration island with Blender.

Run using Blender's --background --factory-startup --python-exit-code 1 --python
options. Everything is generated from analytic functions: no external packages,
textures, or copyrighted asset inputs. The GLB is a reusable asset, not a world.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy


ASSET_ID = "island_calibration"
ANGULAR_SAMPLES = 160
SURFACE_RINGS = 24
ROCK_RINGS = 48
SCHEMA_VERSION = 1


def outline(angle: float) -> tuple[float, float]:
    """Controlled large gestures, with a few softer secondary contour changes."""
    shape = (1.0 + 0.043 * math.sin(3.0 * angle + 0.45)
             + 0.027 * math.cos(5.0 * angle - 0.8)
             + 0.012 * math.sin(9.0 * angle + 0.3))
    return 9.0 * shape * math.cos(angle), 7.0 * shape * math.sin(angle)


def surface_height(x: float, y: float) -> float:
    """Restful topography with a broad rise and shallow saddle; meters."""
    rise = 0.62 * math.exp(-((x + 2.3) ** 2 / 24.0 + (y - 1.0) ** 2 / 16.0))
    saddle = 0.12 * math.exp(-((x - 3.0) ** 2 / 10.0 + (y + 2.0) ** 2 / 12.0))
    fine = 0.025 * math.sin(x * 0.8 + y * 0.35) * math.cos(y * 0.9)
    return 0.20 + rise - saddle + fine


def material(name: str, color: tuple[float, float, float], roughness: float):
    result = bpy.data.materials.new(name)
    result.use_nodes = True
    bsdf = result.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = 0.0
    result.diffuse_color = (*color, 1.0)
    return result


def make_mesh(name: str, vertices: list, faces: list, materials: list,
              material_indices: list, parent):
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    assert not mesh.validate(verbose=False), f"Invalid topology in {name}"
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.parent = parent
    # Geometry is authored in local meters: identity transforms are intentional.
    for mat in materials:
        mesh.materials.append(mat)
    for polygon, material_index in zip(mesh.polygons, material_indices):
        polygon.use_smooth = True
        polygon.material_index = material_index
    mesh.calc_loop_triangles()
    assert all(math.isfinite(component) for vertex in vertices for component in vertex)
    assert all(triangle.area > 1e-8 for triangle in mesh.loop_triangles), name
    return obj


def surface(parent, materials):
    vertices = [(0.0, 0.0, surface_height(0.0, 0.0))]
    for ring in range(1, SURFACE_RINGS + 1):
        radius = ring / SURFACE_RINGS
        for index in range(ANGULAR_SAMPLES):
            angle = math.tau * index / ANGULAR_SAMPLES
            x, y = outline(angle)
            x, y = x * radius, y * radius
            vertices.append((x, y, surface_height(x, y)))
    faces = []
    for index in range(ANGULAR_SAMPLES):
        faces.append((0, 1 + index, 1 + (index + 1) % ANGULAR_SAMPLES))
    for ring in range(SURFACE_RINGS - 1):
        inner = 1 + ring * ANGULAR_SAMPLES
        outer = inner + ANGULAR_SAMPLES
        for index in range(ANGULAR_SAMPLES):
            next_index = (index + 1) % ANGULAR_SAMPLES
            faces.append((inner + index, outer + index,
                          outer + next_index, inner + next_index))
    # Broad patches keep the surface readable; these calibrate material slots,
    # not final grass texture density or a vegetation implementation.
    indices = []
    for face in faces:
        x = sum(vertices[i][0] for i in face) / len(face)
        y = sum(vertices[i][1] for i in face) / len(face)
        patch = math.sin(x * 0.43 + y * 0.19) + 0.6 * math.cos(y * 0.62 - x * 0.11)
        indices.append(1 if patch > 0.7 else 0)
    return make_mesh("Surface", vertices, faces, materials, indices, parent)


def rock_shell(parent, materials):
    vertices = []
    for ring in range(ROCK_RINGS):
        depth = ring / ROCK_RINGS
        for index in range(ANGULAR_SAMPLES):
            angle = math.tau * index / ANGULAR_SAMPLES
            x, y = outline(angle)
            # Shared rim is bit-identical to Surface's perimeter. Below it,
            # shoulders, strata and restrained vertical ribs sculpt the mass.
            taper = (1.0 - depth) ** 0.69
            shoulder = 1.0 - 0.11 * math.exp(-((depth - 0.27) / 0.11) ** 2)
            strata = 0.025 * math.sin(depth * 39.0 + 0.5 * math.sin(angle * 3.0))
            ribs = (0.046 * math.sin(angle * 8.0 + 0.3)
                    + 0.026 * math.sin(angle * 13.0 - depth * 2.0))
            gesture = 0.07 * math.sin(angle * 2.0 + depth * 3.0)
            relief = math.sin(math.pi * depth) * (ribs + strata + gesture)
            factor = taper * shoulder * (1.0 + relief)
            # The shoulder's Gaussian tail is nonzero at depth=0. Preserve
            # the shared rim explicitly instead of shrinking it by ~2.5mm.
            if ring == 0:
                factor = 1.0
            offset_x = 1.65 * depth ** 1.5
            offset_y = -0.75 * depth ** 1.3
            z = surface_height(x, y) * (1.0 - depth) ** 3 - 7.8 * depth
            vertices.append((x * factor + offset_x, y * factor + offset_y, z))
    tip_index = len(vertices)
    vertices.append((1.65, -0.75, -7.8))
    faces, indices = [], []
    for ring in range(ROCK_RINGS - 1):
        upper = ring * ANGULAR_SAMPLES
        lower = upper + ANGULAR_SAMPLES
        depth = (ring + 0.5) / ROCK_RINGS
        for index in range(ANGULAR_SAMPLES):
            next_index = (index + 1) % ANGULAR_SAMPLES
            faces.append((upper + index, lower + index,
                          lower + next_index, upper + next_index))
            angle = math.tau * (index + 0.5) / ANGULAR_SAMPLES
            band = depth + 0.024 * math.sin(angle * 3.0 + 0.4)
            if depth < 0.047:
                slot = 3  # Moss contact band at the rim.
            elif 0.18 < band < 0.235 or 0.47 < band < 0.50 or band > 0.80:
                slot = 2  # A few geological layers, not equally spaced stripes.
            elif math.sin(angle * 6.0 + depth * 2.0) > 0.65:
                slot = 1  # Ivory mineral ribs catch the key light.
            else:
                slot = 0
            indices.append(slot)
    bottom = (ROCK_RINGS - 1) * ANGULAR_SAMPLES
    for index in range(ANGULAR_SAMPLES):
        faces.append((bottom + index, tip_index,
                      bottom + (index + 1) % ANGULAR_SAMPLES))
        indices.append(2)
    return make_mesh("RockShell", vertices, faces, materials, indices, parent)


def write_catalog(root: Path, objects: list, glb_path: Path):
    vertices = [tuple(vertex.co) for obj in objects for vertex in obj.data.vertices]
    bounds_min = [min(vertex[axis] for vertex in vertices) for axis in range(3)]
    bounds_max = [max(vertex[axis] for vertex in vertices) for axis in range(3)]
    # Blender (x, y, z) -> glTF/Godot (x, z, -y).
    godot_min = [bounds_min[0], bounds_min[2], -bounds_max[1]]
    godot_max = [bounds_max[0], bounds_max[2], -bounds_min[1]]
    boundary = []
    for index in range(ANGULAR_SAMPLES):
        angle = math.tau * index / ANGULAR_SAMPLES
        x, y = outline(angle)
        boundary.append([round(x, 6), round(surface_height(x, y), 6), round(-y, 6)])
    catalog = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": ASSET_ID,
        "stage": "pipeline_calibration_not_final_environment_art",
        "generator": "tools/blender/build_calibration_asset.py",
        "source": "assets/source/blender/island_calibration.blend",
        "model": "assets/models/terrain/island_calibration.glb",
        "blender_version": bpy.app.version_string,
        "units": "meters",
        "coordinates": {"source": "Blender +Z up", "runtime": "Godot +Y up, -Z forward",
                        "conversion": "official glTF exporter; (x, y, z) -> (x, z, -y)"},
        "origin": "center of top footprint at Godot y=0; intentional identity transforms",
        "bounds_godot": {"min": godot_min, "max": godot_max},
        "mesh_stats": [{"name": obj.name, "vertices": len(obj.data.vertices),
                        "triangles": len(obj.data.loop_triangles),
                        "material_slots": [mat.name for mat in obj.data.materials]}
                       for obj in objects],
        "triangle_count": sum(len(obj.data.loop_triangles) for obj in objects),
        "boundary_samples_godot": boundary,
        "surface_contract": "Surface and RockShell share all 160 rim positions. Surface data is independent from future editable terrain chunks; this asset does not implement sculpting.",
        "glb_sha256": hashlib.sha256(glb_path.read_bytes()).hexdigest(),
        "limitations": ["No final texture art, UV layout, collision, LODs, vegetation, or gameplay.",
                        "Material patches and sculpted strata calibrate import and lighting only."]
    }
    metadata = glb_path.with_suffix(".asset.json")
    metadata.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print("CALIBRATION_ASSET_OK " + json.dumps({"model": str(glb_path),
          "triangles": catalog["triangle_count"], "sha256": catalog["glb_sha256"]}))


def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path,
                        default=Path(__file__).resolve().parents[2])
    project_root = parser.parse_args(args).project_root.resolve()
    source_path = project_root / "assets/source/blender/island_calibration.blend"
    model_path = project_root / "assets/models/terrain/island_calibration.glb"
    for path in (source_path, model_path):
        path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.context.preferences.filepaths.save_version = 0
    parent = bpy.data.objects.new(ASSET_ID, None)
    bpy.context.collection.objects.link(parent)
    parent["asset_id"] = ASSET_ID
    parent["units"] = "meters"
    parent["stage"] = "pipeline_calibration"
    moss = material("Moss_Sage", (0.19, 0.29, 0.18), 0.88)
    meadow = material("Moss_Light", (0.25, 0.35, 0.20), 0.88)
    limestone = material("Stone_Limestone", (0.47, 0.44, 0.37), 0.79)
    ivory = material("Stone_Ivory", (0.59, 0.56, 0.48), 0.75)
    slate = material("Stone_CoolStrata", (0.29, 0.32, 0.34), 0.84)
    objects = [surface(parent, [moss, meadow]),
               rock_shell(parent, [limestone, ivory, slate, moss])]
    for obj in [parent, *objects]:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.wm.save_as_mainfile(filepath=str(source_path))
    bpy.ops.export_scene.gltf(filepath=str(model_path), export_format="GLB",
                              use_selection=True, export_yup=True,
                              export_apply=True, export_normals=True,
                              export_texcoords=False, export_tangents=False,
                              export_animations=False, export_extras=True,
                              export_materials="EXPORT", export_cameras=False,
                              export_lights=False)
    write_catalog(project_root, objects, model_path)


if __name__ == "__main__":
    main()
