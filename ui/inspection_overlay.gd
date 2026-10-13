# Copyright (c) 2026 spinjitsu12. All rights reserved.
# Express written permission required; see LICENSE.
extends CanvasLayer
## Small, responsive art-review overlay. No gameplay or construction controls.

func _ready() -> void:
	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 48)
	margin.add_theme_constant_override("margin_right", 48)
	margin.add_theme_constant_override("margin_top", 40)
	margin.add_theme_constant_override("margin_bottom", 34)
	margin.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(margin)
	var stack := VBoxContainer.new()
	stack.mouse_filter = Control.MOUSE_FILTER_IGNORE
	margin.add_child(stack)
	add_label(stack, "F L O A T I N G   I S L A N D", 16, Color(0.42, 0.34, 0.2))
	add_label(stack, "Sanctuary", 42, Color(0.12, 0.19, 0.26))
	add_label(stack, "STAGE 01   /   ASSET & LIGHTING STUDY", 12, Color(0.25, 0.33, 0.4))
	var spacer := Control.new()
	spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
	spacer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stack.add_child(spacer)
	add_label(stack, "01   /   SUSPENDED LANDFORM", 17, Color(0.16, 0.23, 0.29))
	add_label(stack, "Original calibration asset · Blender → GLB → Godot", 13, Color(0.25, 0.33, 0.4))
	add_label(stack, "Drag to orbit     /     Scroll to inspect     /     R to reset", 13, Color(0.25, 0.33, 0.4))

func add_label(parent: Node, text: String, size: int, color: Color) -> void:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	label.add_theme_color_override("font_shadow_color", Color(1.0, 1.0, 1.0, 0.25))
	label.add_theme_constant_override("shadow_offset_y", 1)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(label)
