# Copyright (c) 2026 spinjitsu12. All rights reserved.
# Express written permission required; see LICENSE.
#!/usr/bin/env python3
"""Source-to-engine checks; standard library only, no shell execution."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "validation"
SANDBOX_DIAGNOSTICS = (
    "/Library/Application Support/Godot/app_userdata/",
    'Condition "ret != noErr" is true. Returning: ""',
    "Could not open 'user://' directory:", "Could not create ObjectDB Snapshots directory:",
    "/Library/Application Support/Godot/editor_settings-",
)


def executable(kind):
    override = os.environ.get(f"{kind.upper()}_BIN")
    names = [kind, "godot4"] if kind == "godot" else [kind]
    candidates = [override] if override else []
    candidates += [shutil.which(name) for name in names]
    application = "Blender" if kind == "blender" else "Godot"
    candidates += [str(base / f"{application}.app" / "Contents" / "MacOS" / application)
                   for base in (Path("/Applications"), Path.home() / "Applications")]
    if override and not (Path(override).is_file() and os.access(override, os.X_OK)):
        raise RuntimeError(f"{kind.upper()}_BIN is not an executable file: {override}")
    for candidate in candidates:
        if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return str(Path(candidate).resolve())
    raise RuntimeError(f"{kind} not found. Install it or set {kind.upper()}_BIN.")


def run(step, command, marker=None):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (ROOT / "build" / ".gdignore").touch()
    print(f"[{step}] " + " ".join(map(str, command)), flush=True)
    completed = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, timeout=240)
    (OUTPUT / f"{step}.log").write_text(completed.stdout)
    print(completed.stdout, end="")
    if completed.returncode != 0:
        raise RuntimeError(f"{step} failed with exit {completed.returncode}; see build/validation/{step}.log")
    if marker and marker not in completed.stdout:
        raise RuntimeError(f"{step} did not emit its completion marker {marker}")
    # Godot can return 0 on script errors: the exit status alone is insufficient.
    if "SCRIPT ERROR:" in completed.stdout or "SHADER ERROR:" in completed.stdout:
        raise RuntimeError(f"{step} reported a script/shader error")
    diagnostics = [line for line in completed.stdout.splitlines() if line.startswith("ERROR:")]
    unexpected = [line for line in diagnostics if not any(known in line for known in SANDBOX_DIAGNOSTICS)]
    if unexpected:
        raise RuntimeError(f"{step} reported unexpected engine errors: " + "; ".join(unexpected))
    return {"step": step, "exit_code": completed.returncode,
            "log": f"build/validation/{step}.log", "sandbox_diagnostics": diagnostics}


def perform(step, view="hero"):
    if step == "build":
        return run(step, [executable("blender"), "--background", "--factory-startup",
                          "--python-exit-code", "1", "--python",
                          str(ROOT / "tools/blender/build_calibration_asset.py")], "CALIBRATION_ASSET_OK")
    godot = executable("godot")
    base = [godot, "--path", str(ROOT), "--log-file", str(OUTPUT / f"{step}-engine.log")]
    if step == "import":
        return run(step, base + ["--headless", "--editor", "--import", "--quit"])
    if step == "test":
        run("asset-integrity", [sys.executable, str(ROOT / "tests/validate_asset.py")], "ASSET_CONTAINER_OK")
        return run(step, base + ["--headless", "--script", "res://tests/foundation_test.gd"], "FOUNDATION_TESTS_OK")
    capture = OUTPUT / ("foundation.png" if view == "hero" else f"foundation-{view}.png")
    # Delete only our own stale capture so a failed run cannot appear successful.
    if capture.exists():
        capture.unlink()
    driver = "metal" if sys.platform == "darwin" else "vulkan"
    result = run(step, base + ["--rendering-method", "forward_plus", "--rendering-driver", driver,
                              "--", f"--capture={capture}", f"--view={view}"], "FOUNDATION_CAPTURE status=0")
    if not capture.is_file():
        raise RuntimeError("Render returned without creating a screenshot")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "import", "test", "render", "all"])
    parser.add_argument("--view", choices=["hero", "reverse", "top"], default="hero",
                        help="Native render review angle; ignored by non-render steps")
    options = parser.parse_args()
    sequence = ["build", "import", "test", "render"] if options.command == "all" else [options.command]
    results = [perform(step, options.view) for step in sequence]
    (OUTPUT / f"{options.command}-result.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"PIPELINE FAILED: {error}", file=sys.stderr)
        sys.exit(1)
