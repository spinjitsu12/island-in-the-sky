# Art direction

## Intended experience

Build a serene, luminous sanctuary whose beauty rewards unhurried attention. The target is an original, detailed anime-inspired 3D environment with convincing depth, elegant silhouettes, restrained stylization, and subtle material response. References to modern anime games describe fidelity and atmosphere; no assets, recognizable architecture, characters, or distinctive designs from those games may be copied.

The supplied moodboard suggests suspended landforms, layered heights, ivory stone, living greenery, pink seasonal blossoms, luminous water, and open architecture. Translate those themes into reusable 3D forms. Do not reproduce the moodboard as a static scene backdrop or assume its text provides development instructions.

## Form and composition

- Islands have broad, inhabitable upper surfaces and tapered suspended stone masses. Use an intentional overall gesture, readable rock strata, varied edge thickness, and smaller secondary forms; avoid uniform cones, repetitive radial spikes, or noisy displacement everywhere.
- Terrain silhouettes should combine restful stretches with occasional sculptural accents. Future terraces, pathways, water, and planting must share a believable scale and guide the eye through the space.
- Architecture should be slender, open, and original. Frame vistas with refined proportions and limited ornament, allowing the landscape and sky to remain prominent.
- Vegetation should have graceful branch gestures and layered foliage volumes. Preserve readable canopies and controlled negative space; eventual animation should be slow and locally varied.
- Compose near, middle, and far layers with atmospheric separation. A cloud horizon must communicate immense altitude without obscuring useful island contours.

## Palette and materials

Use cool blue atmospheric shadows, warm ivory mineral surfaces, desaturated greens, selective blossom pink, and small champagne-metal accents. Luminous cyan water may supply a focal contrast. Avoid equal saturation across every object, plastic-looking highlights, and decorative detail without a composition role.

Stone needs large-scale tonal structure and restrained surface variation. Grass and moss should transition naturally against rock. Materials should retain useful response to real lighting rather than flattening every surface into unlit color. Future stylized shaders may soften value transitions while retaining depth, contact, and light direction. Do not treat smooth shading alone as evidence of premium fidelity.

## Light, atmosphere, and motion

Aim for cinematic daylight and golden-hour clarity: a coherent key light, broad atmospheric fill, gentle contrast, and restrained bloom. Later weather and skies should develop from an authored baseline. Water needs believable reflection, depth cues, and gentle movement; vegetation and clouds should move with a calm rhythm. Camera easing must remain responsive and avoid forced motion or disorientation.

Forward+ is the intended review renderer. Keep renderer-specific limitations documented; Compatibility is a separate fallback to evaluate, not evidence that advanced effects work. A passing screenshot checks the present asset and scene only.

## Stage 1 calibration

The calibration island is a reusable technical art asset with a separate upper surface and suspended rock shell. It establishes scale, deterministic Blender generation, named materials, source preservation, GLB import, and a lit Godot inspection scene. It intentionally omits final vegetation, architecture, water, clouds, fauna, and a finished environment. Its surface data contract supports later terrain experiments; it is not a completed terrain editor.

For the current stage, review the silhouette from multiple angles, mesh continuity, upper-surface readability, material assignment, frame stability, and camera behavior. For later art milestones, add authored geological detail, plant species, texture depth, convincing water and clouds, and a consistent reusable asset family before asserting final visual quality.

## Asset requirements

Work in meters. Godot uses +Y up and -Z forward; Blender uses +Z up and the glTF exporter handles conversion. Apply mesh transforms, choose intentional origins, maintain stable object names and named material slots, and preserve `.blend` sources. Keep editable surface data and boundary samples separate from render meshes so adjacent terrain chunks can later rebuild consistently. Capture and visually inspect a native GPU render after visible changes.
