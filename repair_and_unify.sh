#!/usr/bin/env bash
set -eu

DRY_RUN=1
APPLY=0
BACKUP_SUFFIX=".bak.$(date +%Y%m%d%H%M%S)"

usage(){
  cat <<EOF
Usage: $0 [--apply | --dry-run]

--dry-run  : (default) Print planned actions without modifying files
--apply    : Execute changes (destructive operations will backup first)
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --apply) DRY_RUN=0; APPLY=1; shift ;;
    --dry-run) DRY_RUN=1; APPLY=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1"; usage; exit 2 ;;
  esac
done

echo "[*] INITIATING LUCID EMPIRE REPAIR SEQUENCE..."

# Standard target
TARGET="LUCID_EMPIRE"
ALT="LUCID-EMPIRE"

plan_action(){
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[DRY-RUN] $1"
  else
    echo "[APPLY] $1"
    eval "$1"
  fi
}

# 1. CLEANUP: if alternate folder exists, offer to migrate contents
if [ -d "$ALT" ]; then
  echo "[*] Found legacy folder: $ALT -> will migrate into $TARGET"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[DRY-RUN] Would merge $ALT -> $TARGET (backup existing target if any)"
  else
    if [ -d "$TARGET" ]; then
      echo "[APPLY] Backing up existing $TARGET to ${TARGET}${BACKUP_SUFFIX}"
      mv "$TARGET" "${TARGET}${BACKUP_SUFFIX}"
    fi
    echo "[APPLY] Moving $ALT -> $TARGET"
    mv "$ALT" "$TARGET"
  fi
fi

# 2. CREATE CANONICAL STRUCTURE
plan_action "mkdir -p $TARGET/{core,engine,interface,runtime,storage/profiles,bin}"

# 3. MIGRATE CAPABILITIES (Rescue Phase)
# human_mouse -> core/mouse.py
if [ -f "modules/human_mouse.py" ]; then
  plan_action "cp modules/human_mouse.py $TARGET/core/mouse.py"
  plan_action "echo '[+] Migrated HumanMouse'"
fi

# burner -> core/burner.py
if [ -f "tools/burner.py" ]; then
  plan_action "cp tools/burner.py $TARGET/core/burner.py"
  plan_action "echo '[+] Migrated Burner'"
fi

# tls_mimic -> core/tls.py (or create stub)
if [ -f "core/tls_mimic.py" ]; then
  plan_action "cp core/tls_mimic.py $TARGET/core/tls.py"
  plan_action "echo '[+] Migrated TLS mimic'"
else
  if [ ! -f "$TARGET/core/tls.py" ]; then
    plan_action "touch $TARGET/core/tls.py"
    plan_action "echo '[!] Created TLS stub'"
  fi
fi

# commerce -> core/commerce.py
if [ -f "core/commerce_injector.py" ]; then
  plan_action "cp core/commerce_injector.py $TARGET/core/commerce.py"
  plan_action "echo '[+] Migrated CommerceInjector'"
fi

# dashboard -> interface/index.html
if [ -f "templates/dashboard.html" ]; then
  plan_action "cp templates/dashboard.html $TARGET/interface/index.html"
  plan_action "echo '[+] Migrated Dashboard'"
fi

# 4. RUNTIME SETUP: copy sovereign Dockerfile if present
if [ -f "docker/Dockerfile.sovereign" ]; then
  plan_action "cp docker/Dockerfile.sovereign $TARGET/runtime/Dockerfile"
else
  plan_action "cat > $TARGET/runtime/Dockerfile <<'EOF'\nFROM python:3.11-slim\nRUN apt-get update && apt-get install -y libfaketime xvfb\nCMD ['python3', '/app/app.py']\nEOF"
fi

# 5. FINALIZE PYTHON PACKAGE
plan_action "touch $TARGET/__init__.py"
plan_action "touch $TARGET/core/__init__.py"

echo "[+] REPAIR SEQUENCE: Completed plan. Dry-run=$DRY_RUN"

if [ "$DRY_RUN" -eq 1 ]; then
  echo "Run with --apply to perform changes (backups will be created where applicable)."
fi
