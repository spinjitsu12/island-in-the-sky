# Copyright (c) 2026 spinjitsu12. All rights reserved.
# Express written permission required; see LICENSE.
extends Node3D

const MODEL = "res://assets/models/terrain/island_calibration.glb"
const CAMERA = preload("res://scripts/inspection/orbit_camera.gd")
const REVIEW_UI = preload("res://ui/inspection_overlay.gd")

func _ready() -> void:
	var scene := load(MODEL) as PackedScene
	if scene == null:
		push_error("Calibration GLB unavailable. Run python3 tools/pipeline.py import")
		get_tree().quit(1)
		return
	add_child(scene.instantiate())
	var camera := Camera3D.new()
	camera.set_script(CAMERA)
	camera.fov = 45.0
	camera.near = 0.1
	camera.far = 2000.0
	for argument in OS.get_cmdline_user_args():
		if argument == "--view=reverse":
			camera.desired_yaw = 3.72
			camera.yaw = 3.72
		if argument == "--view=top":
			camera.desired_pitch = 1.0
			camera.pitch = 1.0
	add_child(camera)
	camera.current = true
	var key := DirectionalLight3D.new()
	key.rotation_degrees = Vector3(-32, -38, 0)
	key.light_color = Color(1.0, 0.85, 0.69)
	key.light_energy = 1.2
	key.shadow_enabled = true
	add_child(key)
	var fill := DirectionalLight3D.new()
	fill.rotation_degrees = Vector3(-22, 125, 0)
	fill.light_color = Color(0.59, 0.73, 1.0)
	fill.light_energy = 0.25
	add_child(fill)
	var environment := Environment.new()
	environment.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var material := ShaderMaterial.new()
	material.shader = preload("res://assets/shaders/calibration_sky.gdshader")
	sky.sky_material = material
	environment.sky = sky
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color(0.68, 0.77, 0.9)
	environment.ambient_light_energy = 0.3
	environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	if RenderingServer.get_current_rendering_method() == "forward_plus":
		environment.ssao_enabled = true
		environment.ssao_radius = 1.0
		environment.ssao_intensity = 1.1
		environment.glow_enabled = true
	var world := WorldEnvironment.new()
	world.environment = environment
	add_child(world)
	var overlay := CanvasLayer.new()
	overlay.set_script(REVIEW_UI)
	add_child(overlay)
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture="):
			capture.call_deferred(argument.trim_prefix("--capture="))

func capture(path: String) -> void:
	for frame in range(24):
		await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var image := get_viewport().get_texture().get_image()
	DirAccess.make_dir_recursive_absolute(path.get_base_dir())
	var status := image.save_png(path)
	print("FOUNDATION_CAPTURE status=", status, " size=", image.get_size(), " renderer=", RenderingServer.get_current_rendering_method(), " adapter=", RenderingServer.get_video_adapter_name())
	get_tree().quit(0 if status == OK else 1)
