# Copyright (c) 2026 spinjitsu12. All rights reserved.
# Express written permission required; see LICENSE.
extends SceneTree

const CHUNK = preload("res://scripts/terrain/terrain_chunk_data.gd")
const ORBIT = preload("res://scripts/inspection/orbit_camera.gd")
var failures: Array[String] = []
var checks := 0

func expect(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures.append(message)

func _initialize() -> void:
	call_deferred("run_tests")

func run_tests() -> void:
	var sample := func(location: Vector2) -> float: return sin(location.x * 0.2) + cos(location.y * 0.3)
	var center = CHUNK.new()
	center.configure(Vector2i.ZERO, 16, 0.5)
	center.sample_from_world(sample)
	var east = CHUNK.new()
	east.configure(Vector2i(1, 0), 16, 0.5)
	east.sample_from_world(sample)
	var north = CHUNK.new()
	north.configure(Vector2i(0, -1), 16, 0.5)
	north.sample_from_world(sample)
	expect(center.is_valid(), "Center sample lattice invalid")
	expect(center.heights.size() == 289, "Inclusive sample lattice size wrong")
	expect(center.boundary(&"east") == east.boundary(&"west"), "East shared boundary is discontinuous")
	expect(center.boundary(&"north") == north.boundary(&"south"), "Negative-grid boundary is discontinuous")
	expect(center.world_sample(Vector2i(16, 4)) == east.world_sample(Vector2i(0, 4)), "Shared boundary world coordinates disagree")
	var before: float = east.heights[0]
	center.heights[0] = 99.0
	expect(east.heights[0] == before, "Chunk resources alias sample storage")
	east.heights[0] = NAN
	expect(not east.is_valid(), "Nonfinite height accepted")
	east.heights[0] = before
	east.sample_spacing = INF
	expect(not east.is_valid(), "Nonfinite spacing accepted")
	center.heights.resize(3)
	expect(not center.is_valid(), "Malformed data accepted")
	var packed := load("res://assets/models/terrain/island_calibration.glb") as PackedScene
	expect(packed != null, "GLB import failed")
	if packed != null:
		var asset := packed.instantiate()
		root.add_child(asset)
		var meshes := asset.find_children("*", "MeshInstance3D", true, false)
		expect(meshes.size() >= 2, "Terrain surface and rock shell are not separate meshes")
		var surface_found := false
		var rock_found := false
		var vertices := 0
		var surface_positions := {}
		var rock_positions := {}
		for instance in meshes:
			surface_found = surface_found or "surface" in instance.name.to_lower()
			rock_found = rock_found or "rock" in instance.name.to_lower()
			expect(instance.scale.is_equal_approx(Vector3.ONE), "Mesh scale not applied: " + instance.name)
			for surface in range(instance.mesh.get_surface_count()):
				expect(instance.mesh.surface_get_material(surface) != null, "Imported surface lacks a material")
				var positions: PackedVector3Array = instance.mesh.surface_get_arrays(surface)[Mesh.ARRAY_VERTEX]
				vertices += positions.size()
				for point in positions:
					var key := position_key(point)
					if "surface" in instance.name.to_lower(): surface_positions[key] = point
					if "rock" in instance.name.to_lower(): rock_positions[key] = point
			var bounds: AABB = instance.mesh.get_aabb()
			expect(bounds.size.length() > 1.0 and bounds.size.length() < 40.0, "Asset scale is not in intended meter range")
			if "rock" in instance.name.to_lower():
				expect(bounds.position.y < -3.0, "Suspended rock is not below surface after glTF axis conversion")
		expect(surface_found and rock_found, "Stable surface/rock object names missing")
		expect(vertices > 1000, "Calibration model unexpectedly sparse")
		var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://assets/models/terrain/island_calibration.asset.json"))
		var shared_rim := true
		for point in manifest.boundary_samples_godot:
			var expected := Vector3(point[0], point[1], point[2])
			var matched := contains_position(surface_positions, expected) and contains_position(rock_positions, expected)
			if not matched and shared_rim:
				print("RIM_MISMATCH expected=", expected, " surface_distance=", nearest_distance(surface_positions, expected), " rock_distance=", nearest_distance(rock_positions, expected))
			shared_rim = shared_rim and matched
		expect(shared_rim, "Imported surface/rock rim differs from manifest; crack risk")
		print("ASSET_INSPECTION meshes=", meshes.size(), " vertices=", vertices)
		asset.queue_free()
	var camera := Camera3D.new()
	camera.set_script(ORBIT)
	root.add_child(camera)
	var scroll := InputEventMouseButton.new()
	scroll.button_index = MOUSE_BUTTON_WHEEL_UP
	scroll.pressed = true
	for i in range(100): camera._unhandled_input(scroll)
	expect(is_equal_approx(camera.desired_distance, camera.minimum_distance), "Camera minimum zoom bound failed")
	scroll.button_index = MOUSE_BUTTON_WHEEL_DOWN
	for i in range(100): camera._unhandled_input(scroll)
	expect(is_equal_approx(camera.desired_distance, camera.maximum_distance), "Camera maximum zoom bound failed")
	camera.dragging = true
	var motion := InputEventMouseMotion.new()
	motion.relative = Vector2(0, 10000)
	camera._unhandled_input(motion)
	expect(camera.desired_pitch <= 1.1, "Camera flips beyond pitch limit")
	camera.distance = 29.0
	camera.desired_distance = 40.0
	for i in range(60): camera._process(1.0 / 60.0)
	var at_sixty: float = camera.distance
	camera.distance = 29.0
	for i in range(30): camera._process(1.0 / 30.0)
	expect(absf(camera.distance - at_sixty) < 0.0001, "Camera easing changes with frame rate")
	expect(absf(camera.distance - camera.desired_distance) < 0.01, "Camera easing does not converge")
	camera.queue_free()
	if failures.is_empty():
		print("FOUNDATION_TESTS_OK checks=", checks)
		quit(0)
	else:
		for failure in failures: push_error(failure)
		quit(1)

func position_key(point: Vector3) -> Vector3i:
	return Vector3i(roundi(point.x * 1000), roundi(point.y * 1000), roundi(point.z * 1000))

func contains_position(positions: Dictionary, point: Vector3) -> bool:
	# Search neighboring bins: rounding a binary float near a bin boundary
	# must not create a false crack. Distance is the actual contract assertion.
	var key := position_key(point)
	for x in range(-1, 2):
		for y in range(-1, 2):
			for z in range(-1, 2):
				var candidate := key + Vector3i(x, y, z)
				if positions.has(candidate) and positions[candidate].distance_to(point) < 0.0001:
					return true
	return false

func nearest_distance(positions: Dictionary, point: Vector3) -> float:
	var distance := INF
	for candidate in positions.values():
		distance = minf(distance, candidate.distance_to(point))
	return distance
