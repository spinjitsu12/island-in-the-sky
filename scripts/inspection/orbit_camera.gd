# Copyright (c) 2026 spinjitsu12. All rights reserved.
# Express written permission required; see LICENSE.
extends Camera3D
## Editor-independent review camera, deliberately not a player controller.

@export var target := Vector3(0, -2.0, 0)
@export var minimum_distance := 16.0
@export var maximum_distance := 48.0
var desired_yaw := 0.58
var desired_pitch := 0.29
var desired_distance := 29.0
var yaw := desired_yaw
var pitch := desired_pitch
var distance := desired_distance
var dragging := false

func _ready() -> void:
	position_camera()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT or event.button_index == MOUSE_BUTTON_RIGHT:
			dragging = event.pressed
		if event.pressed and event.button_index == MOUSE_BUTTON_WHEEL_UP:
			desired_distance = maxf(minimum_distance, desired_distance - 1.5)
		if event.pressed and event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			desired_distance = minf(maximum_distance, desired_distance + 1.5)
	if event is InputEventMouseMotion and dragging:
		desired_yaw -= event.relative.x * 0.004
		desired_pitch = clampf(desired_pitch + event.relative.y * 0.003, -0.15, 1.1)
	if event is InputEventKey and event.pressed and event.keycode == KEY_R:
		desired_yaw = 0.58
		desired_pitch = 0.29
		desired_distance = 29.0

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_WINDOW_FOCUS_OUT:
		dragging = false

func _process(delta: float) -> void:
	var weight := 1.0 - exp(-10.0 * delta)
	yaw = lerp_angle(yaw, desired_yaw, weight)
	pitch = lerpf(pitch, desired_pitch, weight)
	distance = lerpf(distance, desired_distance, weight)
	position_camera()

func position_camera() -> void:
	position = target + Vector3(sin(yaw) * cos(pitch), sin(pitch), cos(yaw) * cos(pitch)) * distance
	look_at(target)
