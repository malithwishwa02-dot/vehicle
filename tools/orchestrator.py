#!/usr/bin/env python3
"""
Orchestrator CLI: single entrypoint to run the full pipeline or individual stages.
Usage examples:
  python tools/orchestrator.py run --uuid 37ab... --age-days 90 --seed 123 --inject-purchases 3 --enrich
  python tools/orchestrator.py dilate --profile generated_profiles/37ab... --days 90 --target 2000
  python tools/orchestrator.py package --profile generated_profiles/37ab... --include-sensitive
  python tools/orchestrator.py dump-history --profile generated_profiles/37ab... --out history.csv
  python tools/orchestrator.py push --message "Add orchestrator"
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def run_fabricate(args):
    cmd = [PY, str(ROOT / 'fabricate_identity.py'), '--uuid', args.uuid, '--age-days', str(args.age_days), '--seed', str(args.seed)]
    if args.force:
        cmd.append('--force')
    if args.inject_purchases and args.inject_purchases > 0:
        cmd.extend(['--inject-purchases', str(args.inject_purchases)])
    if args.enrich:
        cmd.append('--enrich')
    if args.real_leveldb:
        cmd.append('--real-leveldb')
    print('[ORCH] Running fabricate_identity:', ' '.join(cmd))
    subprocess.check_call(cmd)


def run_dilate(args):
    cmd = [PY, str(ROOT / 'time_dilator.py'), '--profile', args.profile, '--days-back', str(args.days), '--target', str(args.target), '--seed', str(args.seed or '')]
    print('[ORCH] Running Time Dilator:', ' '.join(cmd))
    subprocess.check_call(cmd)


def run_enrich(args):
    cmd = [PY, str(ROOT / 'scripts' / 'run_enrichment.py')]
    print('[ORCH] Running enrichment scripts')
    subprocess.check_call(cmd)


def run_package(args):
    cmd = [PY, str(ROOT / 'deploy_to_mlx.py'), '--profile', args.profile, '--out', args.out]
    if args.include_sensitive:
        cmd.append('--include-sensitive')
    print('[ORCH] Packaging profile:', ' '.join(cmd))
    subprocess.check_call(cmd)


def run_dump_history(args):
    cmd = [PY, str(ROOT / 'tools' / 'dump_history.py'), '--profile', args.profile]
    if args.out:
        cmd.extend(['--out', args.out])
    if args.limit:
        cmd.extend(['--limit', str(args.limit)])
    print('[ORCH] Dumping history:', ' '.join(cmd))
    subprocess.check_call(cmd)


def run_push(args):
    print('[ORCH] Committing and pushing changes')
    subprocess.check_call(['git', 'add', '.'])
    subprocess.check_call(['git', 'commit', '-m', args.message or 'orchestrator: automated commit'])
    subprocess.check_call(['git', 'push'])


def run_generate(args):
    """Run fabricate_identity then copy the final profile folder to out-dir."""
    # Run the normal fabricate flow
    run_fabricate(args)

    # Determine artifact path
    artifact = ROOT / 'generated_profiles' / args.uuid
    if not artifact.exists():
        print('[ORCH] ERROR: Generated profile folder not found:', artifact)
        return

    if args.out_dir:
        import shutil
        out_dir = Path(args.out_dir)
        if out_dir.exists():
            print(f"[ORCH] Removing existing out-dir: {out_dir}")
            shutil.rmtree(out_dir)
        print(f"[ORCH] Copying artifact to: {out_dir}")
        shutil.copytree(artifact, out_dir)
        print(f"[ORCH] Profile copied to {out_dir}")
    else:
        print(f"[ORCH] Generated profile available at: {artifact}")

    if args.package:
        pkg_name = f"mlx_import_package_generated_{args.uuid}"
        pkg_args = argparse.Namespace(profile=str(artifact), out=pkg_name, include_sensitive=args.include_sensitive)
        run_package(pkg_args)
        print('[ORCH] Packaging complete')


def main():
    ap = argparse.ArgumentParser(prog='orchestrator')
    sub = ap.add_subparsers(dest='cmd')

    p_run = sub.add_parser('run', help='Run full fabricate pipeline')
    p_run.add_argument('--uuid', default='37ab1612-c285-4314-b32a-6a06d35d6d84')
    p_run.add_argument('--age-days', type=int, default=90)
    p_run.add_argument('--seed', type=int, default=123)
    p_run.add_argument('--inject-purchases', type=int, default=0)
    p_run.add_argument('--enrich', action='store_true')
    p_run.add_argument('--force', action='store_true')
    p_run.add_argument('--real-leveldb', action='store_true')

    p_dilate = sub.add_parser('dilate', help='Run Time Dilator')
    p_dilate.add_argument('--profile', required=True)
    p_dilate.add_argument('--days', type=int, default=90)
    p_dilate.add_argument('--target', type=int, default=2000)
    p_dilate.add_argument('--seed', type=int, default=123)

    p_enrich = sub.add_parser('enrich', help='Run enrichment (Top Sites/Autofill/Shortcuts/LS)')

    p_package = sub.add_parser('package', help='Package profile into ZIP')
    p_package.add_argument('--profile', required=True)
    p_package.add_argument('--out', default='mlx_import_package')
    p_package.add_argument('--include-sensitive', action='store_true')

    p_dump = sub.add_parser('dump-history', help='Dump history to CSV')
    p_dump.add_argument('--profile', required=True)
    p_dump.add_argument('--out')
    p_dump.add_argument('--limit', type=int)

    p_push = sub.add_parser('push', help='Commit and push current repo changes')
    p_push.add_argument('--message', help='Commit message')

    p_gen = sub.add_parser('generate', help='Run full pipeline and export local profile folder')
    p_gen.add_argument('--uuid', default='37ab1612-c285-4314-b32a-6a06d35d6d84')
    p_gen.add_argument('--age-days', type=int, default=90)
    p_gen.add_argument('--seed', type=int, default=123)
    p_gen.add_argument('--inject-purchases', type=int, default=0)
    p_gen.add_argument('--enrich', action='store_true')
    p_gen.add_argument('--force', action='store_true')
    p_gen.add_argument('--real-leveldb', action='store_true')
    p_gen.add_argument('--out-dir', help='Path to copy final profile folder to')
    p_gen.add_argument('--package', action='store_true', help='Also create a package/zip of the profile')
    p_gen.add_argument('--include-sensitive', action='store_true', help='Include sensitive DBs when packaging')

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        sys.exit(1)

    if args.cmd == 'run':
        run_fabricate(args)
    elif args.cmd == 'dilate':
        run_dilate(args)
    elif args.cmd == 'enrich':
        run_enrich(args)
    elif args.cmd == 'package':
        run_package(args)
    elif args.cmd == 'dump-history':
        run_dump_history(args)
    elif args.cmd == 'push':
        run_push(args)
    elif args.cmd == 'generate':
        run_generate(args)


if __name__ == '__main__':
    main()
