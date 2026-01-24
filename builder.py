#!/usr/bin/env python3
"""builder.py

Safe builder for assembling Lucid Empire from local or remote sources.
Features:
- Dry-run mode (default)
- Optional cloning of remote repos via --clone
- Safe backups when applying changes
- Rebranding text replacement with clear logging
"""
from pathlib import Path
import argparse
import logging
import shutil
import sys
import tempfile
import subprocess
import os

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("builder")

DEFAULT_DST = Path("./LUCID_EMPIRE")
REPLACEMENTS = {
    "Camoufox": "LucidBrowser",
    "camoufox": "lucid",
}
TEXT_EXTS = {".py", ".md", ".json", ".js", ".html", ".css", ".txt"}


def replace_in_file(path: Path, replacements: dict) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return 0
    new = text
    for a, b in replacements.items():
        new = new.replace(a, b)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return 1
    return 0


def rebrand_tree(root: Path, replacements: dict, dry_run: bool = True) -> int:
    changed = 0
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXTS:
            try:
                content = p.read_text(encoding="utf-8")
            except Exception:
                continue
            new = content
            for a, b in replacements.items():
                new = new.replace(a, b)
            if new != content:
                changed += 1
                if dry_run:
                    log.info("[DRY] Would rebrand: %s", p)
                else:
                    p.write_text(new, encoding="utf-8")
                    log.info("Rebranded: %s", p)
    return changed


def copy_tree(src: Path, dst: Path, dry_run: bool = True) -> None:
    if dry_run:
        log.info("[DRY] Would copy tree: %s -> %s", src, dst)
        return
    if dst.exists():
        backup = dst.with_suffix(dst.suffix + ".bak") if dst.suffix else Path(str(dst) + ".bak")
        log.info("Backing up existing %s -> %s", dst, backup)
        if backup.exists():
            shutil.rmtree(backup)
        shutil.move(str(dst), str(backup))
    shutil.copytree(src, dst)
    log.info("Copied: %s -> %s", src, dst)


def build(dst: Path, camoufox_src: Path | None, vehicle_src: Path | None, resources_dir: Path, dry_run: bool = True, clone: bool = False):
    # Work in a temp directory when cloning
    temp_dirs = []
    try:
        if clone:
            # Clone remote repos into temp dirs
            tmp_cam = Path(tempfile.mkdtemp(prefix="cam_") )
            tmp_vehicle = Path(tempfile.mkdtemp(prefix="veh_"))
            temp_dirs.extend([tmp_cam, tmp_vehicle])
            if camoufox_src is None:
                log.info("Cloning Camoufox into %s", tmp_cam)
                subprocess.run(["git", "clone", "https://github.com/daijro/camoufox.git", str(tmp_cam)], check=True)
            else:
                log.info("Using provided camoufox_src: %s", camoufox_src)
            if vehicle_src is None:
                log.info("Cloning Vehicle into %s", tmp_vehicle)
                subprocess.run(["git", "clone", "https://github.com/malithwishwa02-dot/vehicle.git", str(tmp_vehicle)], check=True)
            else:
                log.info("Using provided vehicle_src: %s", vehicle_src)
            camoufox_src = camoufox_src or tmp_cam
            vehicle_src = vehicle_src or tmp_vehicle

        # Prepare dst
        if dry_run:
            log.info("[DRY] Would create destination: %s", dst)
        else:
            dst.mkdir(parents=True, exist_ok=True)

        # Fuse engine: expect the camoufox package under camoufox/
        if camoufox_src and (camoufox_src / "camoufox").exists():
            src_root = (camoufox_src / "camoufox")
            dst_engine = dst / "core_engine" / "lucid"
            if dry_run:
                log.info("[DRY] Would copy engine from %s to %s", src_root, dst_engine)
            else:
                dst_engine.parent.mkdir(parents=True, exist_ok=True)
                if dst_engine.exists():
                    shutil.rmtree(dst_engine)
                shutil.copytree(src_root, dst_engine)
                log.info("Engine copied to %s", dst_engine)
                # Rebrand text inside
                rebrand_tree(dst_engine, REPLACEMENTS, dry_run=False)
        else:
            log.warning("No camoufox source found; engine step skipped.")

        # Inject vehicle capabilities (mouse, etc.) from vehicle_src
        runtime_dir = dst / "sovereign_runtime"
        if dry_run:
            log.info("[DRY] Would create runtime dir: %s", runtime_dir)
        else:
            runtime_dir.mkdir(parents=True, exist_ok=True)

        if vehicle_src and (vehicle_src / "modules" / "human_mouse.py").exists():
            src_mouse = vehicle_src / "modules" / "human_mouse.py"
            dst_mouse = runtime_dir / "mouse.py"
            if dry_run:
                log.info("[DRY] Would copy human_mouse: %s -> %s", src_mouse, dst_mouse)
            else:
                shutil.copy(src_mouse, dst_mouse)
                log.info("Injected human_mouse into runtime")
        else:
            # Create a stub
            dst_mouse = runtime_dir / "mouse.py"
            if dry_run:
                log.info("[DRY] Would write mouse stub at %s", dst_mouse)
            else:
                dst_mouse.write_text("# Mouse Stub\nclass HumanMouse: pass\n", encoding="utf-8")
                log.info("Wrote mouse stub")

        # Copy resources (launcher and interface) into dst
        if resources_dir and (resources_dir / "launcher.py").exists():
            dst_main = dst / "main.py"
            if dry_run:
                log.info("[DRY] Would copy launcher: %s -> %s", resources_dir / "launcher.py", dst_main)
            else:
                shutil.copy(resources_dir / "launcher.py", dst_main)
                log.info("Copied launcher -> main.py")
        else:
            log.warning("No resources launcher found; dashboard will be limited.")

        if resources_dir and (resources_dir / "interface.html").exists():
            dst_dashboard = dst / "dashboard.html"
            if dry_run:
                log.info("[DRY] Would copy interface: %s -> %s", resources_dir / "interface.html", dst_dashboard)
            else:
                shutil.copy(resources_dir / "interface.html", dst_dashboard)
                log.info("Copied dashboard")
        else:
            log.warning("No interface resource found; created placeholder")
            if not dry_run:
                (dst / "dashboard.html").write_text("<html><body>Dashboard placeholder</body></html>", encoding="utf-8")

        # Create Dockerfile
        df = dst / "Dockerfile"
        dockerfile = """FROM python:3.11-slim
RUN apt-get update && apt-get install -y libfaketime xvfb wget gnupg
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt || true
CMD ["python3", "main.py"]
"""
        if dry_run:
            log.info("[DRY] Would write Dockerfile at %s", df)
        else:
            df.write_text(dockerfile, encoding="utf-8")
            log.info("Dockerfile written")

        log.info("Build (dry_run=%s) finished. Artifact at: %s", dry_run, dst)
        return 0
    finally:
        for d in temp_dirs:
            shutil.rmtree(d, ignore_errors=True)


def parse_args(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--dst", type=Path, default=DEFAULT_DST)
    p.add_argument("--cam-src", type=Path, default=None, help="Local path to camoufox repo root (optional)")
    p.add_argument("--veh-src", type=Path, default=None, help="Local path to vehicle repo root (optional)")
    p.add_argument("--resources", type=Path, default=Path("./resources"), help="Path to resources dir")
    p.add_argument("--dry-run", action="store_true", default=True, dest="dry_run")
    p.add_argument("--apply", action="store_true", default=False, dest="apply")
    p.add_argument("--clone", action="store_true", default=False, help="Clone remote repos into temp dirs before building")
    return p


def main(argv=None):
    p = parse_args(argv)
    args = p.parse_args(argv)
    dry = not args.apply or args.dry_run
    return build(args.dst, args.cam_src, args.veh_src, args.resources, dry_run=dry, clone=args.clone)


if __name__ == "__main__":
    raise SystemExit(main())
