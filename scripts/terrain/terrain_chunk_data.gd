# Copyright (c) 2026 spinjitsu12. All rights reserved.
# Express written permission required; see LICENSE.
class_name TerrainChunkData
extends Resource
## Inclusive lattice of height samples. Rendering and editing are separate clients.
## Adjacent chunks share their final/first sample column or row.

@export var grid_coordinate := Vector2i.ZERO
@export var cells_per_side: int = 16
@export var sample_spacing: float = 1.0
@export var heights := PackedFloat32Array()

func configure(coordinate: Vector2i, cells: int, spacing: float) -> void:
	assert(cells > 0 and is_finite(spacing) and spacing > 0.0, "Chunk dimensions must be positive and finite")
	grid_coordinate = coordinate
	cells_per_side = cells
	sample_spacing = spacing
	heights.resize((cells + 1) * (cells + 1))
	heights.fill(0.0)

func is_valid() -> bool:
	if cells_per_side <= 0 or not is_finite(sample_spacing) or sample_spacing <= 0.0 or heights.size() != (cells_per_side + 1) * (cells_per_side + 1):
		return false
	for height in heights:
		if not is_finite(height):
			return false
	return true

func index(sample: Vector2i) -> int:
	assert(sample.x >= 0 and sample.y >= 0 and sample.x <= cells_per_side and sample.y <= cells_per_side)
	return sample.y * (cells_per_side + 1) + sample.x

func world_sample(sample: Vector2i) -> Vector2:
	return Vector2(grid_coordinate * cells_per_side + sample) * sample_spacing

func sample_from_world(sampler: Callable) -> void:
	for z in range(cells_per_side + 1):
		for x in range(cells_per_side + 1):
			var location = world_sample(Vector2i(x, z))
			heights[index(Vector2i(x, z))] = sampler.call(location)

func boundary(edge: StringName) -> PackedFloat32Array:
	assert(edge in [&"west", &"east", &"north", &"south"])
	var values := PackedFloat32Array()
	for i in range(cells_per_side + 1):
		var sample := Vector2i(0, i)
		match edge:
			&"east": sample = Vector2i(cells_per_side, i)
			&"north": sample = Vector2i(i, 0)
			&"south": sample = Vector2i(i, cells_per_side)
		values.append(heights[index(sample)])
	return values
