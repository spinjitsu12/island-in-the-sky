# Copyright (c) 2026 spinjitsu12. All rights reserved.
# Express written permission required; see LICENSE.
"""Verify interchange integrity independently of Blender and Godot."""
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "assets/models/terrain/island_calibration.glb"


def main():
    manifest = json.loads(MODEL.with_suffix(".asset.json").read_text())
    binary = MODEL.read_bytes()
    magic, version, length = struct.unpack_from("<4sII", binary)
    assert magic == b"glTF" and version == 2 and length == len(binary), "Invalid GLB container"
    json_length, chunk_type = struct.unpack_from("<I4s", binary, 12)
    assert chunk_type == b"JSON", "Missing glTF JSON chunk"
    document = json.loads(binary[20:20 + json_length])
    assert document["asset"]["version"] == "2.0"
    assert manifest["glb_sha256"] == hashlib.sha256(binary).hexdigest(), "Manifest/export mismatch"
    assert (ROOT / manifest["source"]).is_file(), "Editable Blender source missing"
    assert len(document["meshes"]) == 2, "Asset lost surface/shell separation"
    assert {mesh["name"] for mesh in document["meshes"]} == {"SurfaceMesh", "RockShellMesh"}
    assert all("material" in primitive for mesh in document["meshes"] for primitive in mesh["primitives"])
    assert not document.get("images"), "Calibration export unexpectedly depends on image textures"
    assert len(manifest["boundary_samples_godot"]) == 160, "Rim contract missing"
    print("ASSET_CONTAINER_OK source+GLB+manifest integrity verified")


if __name__ == "__main__":
    main()
