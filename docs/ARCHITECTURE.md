# Stage 1 architecture

## Ownership and flow

`tools/blender/build_calibration_asset.py` owns deterministic source generation. Blender exports the same source collection into a runtime GLB; its source and manifest travel with it in Git. Godot's importer owns only the disposable `.godot` cache. `scenes/inspection/asset_inspection.tscn` loads the exported asset and composes lighting, atmosphere, a review camera, and a review overlay. That scene is the current main scene, not a game level.

`tools/pipeline.py` discovers tools, runs them without a shell, writes isolated logs, checks exit status and success markers, and captures the native renderer. It does not install software or alter application settings. Sandboxed editor imports can emit macOS permission diagnostics; inspect logs rather than silently treating every diagnostic as harmless.

## Terrain foundation

`TerrainChunkData` contains a square inclusive lattice: N cells require (N+1)² samples. Its grid coordinate identifies a chunk in a global X/Z lattice; world sample positions derive from integer grid coordinates before conversion to meters. West/east edges iterate Z; north/south edges iterate X. Adjacent equal-resolution chunks have identical shared sample coordinates even for negative grid indices. A world-space height sampler initializes data consistently.

Resources own independent sample arrays and reject malformed/nonfinite data. A future terrain service must enforce equal resolution across neighbors, apply edits to every owner of a shared boundary, rebuild only affected render/collision chunks, and version persistence. This milestone tests the data seam convention; it does not implement edits, streaming, collision, mesh reconstruction, or save files.

The Blender island is an art calibration asset. It is not generated from `TerrainChunkData` yet. Keeping that distinction explicit avoids coupling future terrain tools to a static GLB topology. Stage 3 must add and validate a mesh adapter before claiming dynamically sculptable terrain.

## Future online boundary — design intent only

Online visits to other players' islands are planned for a later stage. Future save data should identify islands and assets with stable IDs and versioned declarative data, independently of scene nodes and render meshes. A future visiting service can then validate and distribute published island snapshots without loading arbitrary remote scripts or executable scenes.

The proposed initial visit mode is read-only: the owner's local editable island, published snapshot, and visitor session are separate states. Publication/access changes belong to the owner and must be checked by the service. Live co-presence, shared editing, and synchronization are not selected or implemented. Keep local creation and persistence independent of network availability. This section introduces no runtime networking or backend dependency.

## Rendering

Forward+ is the desktop review baseline; the runner selects native Metal on macOS and Vulkan elsewhere. The sky shader is a lightweight calibration atmosphere, not final volumetric clouds. SSAO/glow are enabled only for Forward+. Mobile and Compatibility need later parity review. The orbit camera eases with an exponential response independent of frame rate and bounds pitch/distance. UI consumes no orbit input.

## Tracked and local resources

Track editable `.blend`, runtime `.glb`, manifests, GDScript `.uid` files and `.import` settings, source code, reference, and docs. Ignore `.godot`, generated validation logs/images, Blender backup files, and local executable overrides. `.gdignore` keeps source Blender files, reference art, build evidence, and Python tooling out of Godot asset scanning. No reference art is used in the runtime scene.
