#!/usr/bin/env python3
"""F730 Quest data-deploy utility — push the VtMB gamedata tree to a Quest over adb.

Mirrors the engine's mount model (src/engine/virtual_fs.cpp mountGameData): the on-device
destination IS a gamedata root — <dest>/Vampire/... + <dest>/Unofficial_Patch/... — so the
Quest build just points gamedataRoot at it (default /sdcard/vtmb).

Pushes are incremental: a one-roundtrip device manifest (toybox find + stat) diffs against the
source manifest, and only changed files travel — as ONE ustar bundle extracted on-device
(20k+ tiny per-file `adb push` invocations would cost more in process overhead than the data
is worth; toybox tar reads ustar, pax headers are not trusted on-device).

Stdlib only. macOS dev box assumed (bsdtar --format=ustar, innoextract on PATH).

Usage:
  quest_deploy.py scan    --source gamedata [--json]
  quest_deploy.py push    --source gamedata [--dest /sdcard/vtmb] [--dry-run]
                          [--from-installer SETUP.EXE [SETUP2.EXE ...] [--staging DIR]]
  quest_deploy.py verify  --source gamedata [--dest /sdcard/vtmb]

Exit codes: 0 ok · 1 verify diff / post-push mismatch · 2 usage/preflight/anchor failure.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

SOURCE_DIRS = ("Vampire", "Unofficial_Patch")
ANCHOR = os.path.join("Vampire", "pack000.vpk")
BUNDLE_NAME = ".deploy.tar"
DEFAULT_DEST = "/sdcard/vtmb"
DEFAULT_STAGING = os.path.join(".cache", "quest-deploy-staging")

# Excludes (spec: docs/specs/feature-730.md) — Windows x86 binaries our engine never loads,
# saves (both roots; device saves must never be clobbered), OS noise. The tables the engine needs from
# the DLLs are extracted instead (docs/specs/maintenance-2026-11-05-native-tables.md); `derived` is that
# output, excluded so verify ignores it on the device. DLLs already on a device are left alone.
_EXCLUDE_SUBDIRS = {"Vampire": {"dlls", "cl_dlls", "derived", "save"}, "Unofficial_Patch": {"derived", "save"}}
_EXCLUDE_NAMES = {".DS_Store", "Thumbs.db"}


def is_excluded(rel):
    parts = rel.split("/")
    if parts[0] in _EXCLUDE_SUBDIRS and len(parts) > 2 and parts[1] in _EXCLUDE_SUBDIRS[parts[0]]:
        return True
    return parts[-1] in _EXCLUDE_NAMES


def build_manifest(source):
    """rel-path (posix, source-relative) -> (size, mtime-seconds), SOURCE_DIRS minus excludes."""
    manifest, excluded = {}, 0
    for top in SOURCE_DIRS:
        root = os.path.join(source, top)
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            for name in files:
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, source).replace(os.sep, "/")
                if is_excluded(rel):
                    excluded += 1
                    continue
                st = os.stat(full)
                # ustar stores whole-second mtimes — compare in that domain.
                manifest[rel] = (st.st_size, int(st.st_mtime))
    return manifest, excluded


def find_extractor(explicit, search_dirs=("build-vk", "build", "."), path_lookup=shutil.which):
    """The command that extracts the native tables: vtmb-modconv, the one code path (spec)."""
    found = explicit or os.environ.get("VTMB_MODCONV") or path_lookup("vtmb-modconv")
    if not found:
        for folder in search_dirs:
            for name in ("vtmb-modconv", "vtmb-modconv.exe"):
                candidate = os.path.join(folder, name)
                if os.path.isfile(candidate):
                    found = candidate
                    break
            if found:
                break
    if not found:
        die("vtmb-modconv not found. It extracts the tables the engine needs from your vampire.dll. "
            "Build it (cmake --build build-vk --target vtmb-modconv) or pass --extractor PATH.")
    return [os.path.abspath(found) if os.path.isfile(found) else found]


def extract_tables(source, out_root, extractor):
    """rel-path -> (size, mtime) of the extracted files. Stamped with the DLL's mtime so an unchanged
    DLL does not re-push them. A packed or missing DLL stops the deploy here, not at boot."""
    proc = run([*extractor, "extract-tables", source, out_root])
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)
    if proc.returncode != 0:
        die(f"table extraction failed for {source}: {proc.stderr.strip() or proc.stdout.strip()}")
    stamp = int(os.stat(os.path.join(source, "Vampire", "dlls", "vampire.dll")).st_mtime)
    manifest = {}
    derived = os.path.join(out_root, "Vampire", "derived")
    for name in sorted(os.listdir(derived)):
        path = os.path.join(derived, name)
        os.utime(path, (stamp, stamp))
        manifest[f"Vampire/derived/{name}"] = (os.stat(path).st_size, stamp)
    return manifest


def check_anchor(source):
    if not os.path.isfile(os.path.join(source, ANCHOR)):
        die(f"source '{source}' is not a gamedata root — {ANCHOR} not found")


def check_ustar_paths(manifest):
    """ustar hard limits: last component <=100 B, and if the path exceeds 100 B it must split
    into a <=155 B prefix + <=100 B name at a '/'. Violations abort with a named list."""
    over = []
    for rel in manifest:
        raw = rel.encode("utf-8")
        if len(raw) <= 100:
            continue
        name = raw.rsplit(b"/", 1)[-1]
        prefix_ok = False
        for cut in range(len(raw), 0, -1):
            if raw[cut - 1:cut] == b"/" and cut - 1 <= 155 and len(raw) - cut <= 100:
                prefix_ok = True
                break
        if len(name) > 100 or not prefix_ok:
            over.append(rel)
    if over:
        listing = "\n  ".join(sorted(over)[:10])
        die(f"{len(over)} paths exceed ustar limits (100 B name / 155 B prefix):\n  {listing}")


def die(msg, code=2):
    print(f"quest_deploy: error: {msg}", file=sys.stderr)
    sys.exit(code)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# ---------------------------------------------------------------- adb plumbing


def adb_path():
    adb = shutil.which("adb")
    if not adb:
        die("adb not found on PATH (install Android platform-tools)")
    return adb


def adb(*args, check=True):
    proc = run([adb_path(), *args])
    if check and proc.returncode != 0:
        die(f"adb {' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc


def preflight_device():
    proc = adb("get-state", check=False)
    if proc.returncode != 0 or proc.stdout.strip() != "device":
        die("no device connected (connect the Quest via USB, developer mode + adb enabled)")


def device_free_bytes(dest):
    proc = adb("shell", f"df {dest}")
    fields = []
    for line in proc.stdout.splitlines()[1:]:  # skip header
        cols = line.split()
        if len(cols) >= 6:
            fields = cols
    if not fields:
        die(f"could not parse `df {dest}` output: {proc.stdout!r}")
    return int(fields[3]) * 1024  # Available, 1K-blocks


def device_manifest(dest):
    """rel-path -> (size, mtime-seconds) on device; empty when dest does not exist yet."""
    proc = adb("shell", f"find {dest} -type f -exec stat -c '%s %Y %n' {{}} +", check=False)
    if proc.returncode != 0:
        return {}
    prefix = dest.rstrip("/") + "/"
    out = {}
    for line in proc.stdout.splitlines():
        size, _, rest = line.partition(" ")
        mtime, _, path = rest.partition(" ")
        rel = path[len(prefix):] if path.startswith(prefix) else path
        if rel and rel != BUNDLE_NAME and size.isdigit() and mtime.isdigit():
            out[rel] = (int(size), int(mtime))
    return out


def diff_manifests(source_manifest, device_map):
    changed = [rel for rel, sig in source_manifest.items() if device_map.get(rel) != sig]
    # Device-side extras ignore excluded paths too — otherwise on-device saves (excluded
    # from the source manifest by design) would make `verify` red forever.
    extra = [rel for rel in device_map if rel not in source_manifest and not is_excluded(rel)]
    return sorted(changed), sorted(extra)


def write_bundle(bundle, roots):
    """One ustar bundle from files under several roots; `roots` maps rel-path -> its root."""
    try:
        with tarfile.open(bundle, "w", format=tarfile.USTAR_FORMAT) as archive:
            for rel in sorted(roots):
                archive.add(os.path.join(roots[rel], rel), arcname=rel, recursive=False)
    except (OSError, ValueError) as error:
        die(f"tar bundle failed: {error}")


def push_changed(source, dest, changed, dry_run, roots=None):
    total = sum(source_size for _, source_size in changed)
    print(f"push plan: {len(changed)} file(s), {total} bytes -> {dest}")
    if not changed:
        print("device is up to date")
        return
    if dry_run:
        for rel, _ in changed[:20]:
            print(f"  would push {rel}")
        if len(changed) > 20:
            print(f"  ... and {len(changed) - 20} more")
        return
    # Peak demand: the pushed bundle and its extracted payload coexist until `rm` — check
    # ~2.2x payload, not 1.1x. (The same ~payload-sized bundle also lands in macOS TMPDIR.)
    free = device_free_bytes(dest)
    need = int(total * 2.2)
    if free < need:
        die(f"insufficient space on device: {free} free, need ~{need} (bundle + extracted coexist)")
    with tempfile.TemporaryDirectory(prefix="vtmb_deploy_") as tmp:
        bundle = os.path.join(tmp, BUNDLE_NAME)
        write_bundle(bundle, {rel: (roots or {}).get(rel, source) for rel, _ in changed})
        adb("push", bundle, f"{dest}/{BUNDLE_NAME}")
        adb("shell", f"cd {dest} && tar -xf {BUNDLE_NAME} && rm {BUNDLE_NAME}")
    print(f"pushed {len(changed)} file(s), {total} bytes")


# ---------------------------------------------------------------- source staging


def resolve_from_installer(installers, staging):
    innoextract = shutil.which("innoextract")
    if not innoextract:
        die("innoextract not found on PATH (brew install innoextract)")
    os.makedirs(staging, exist_ok=True)
    for exe in installers:
        print(f"extracting {exe} -> {staging} (this can take minutes for the full GOG installer)")
        proc = run([innoextract, "-d", staging, exe])
        if proc.returncode != 0:
            die(f"innoextract failed on {exe}: {proc.stderr.strip() or proc.stdout.strip()}")
    # Locate the game root by the pack000.vpk anchor; shallowest match wins (app/Vampire).
    best = None
    for dirpath, _dirs, files in os.walk(staging):
        if os.path.basename(dirpath) == "Vampire" and "pack000.vpk" in files:
            depth = dirpath.count(os.sep)
            if best is None or depth < best[0]:
                best = (depth, os.path.dirname(dirpath))
    if best is None:
        die(f"no Vampire/pack000.vpk found under {staging} — is that the GOG Bloodlines installer?")
    root = best[1]
    if not os.path.isdir(os.path.join(root, "Unofficial_Patch")):
        print("quest_deploy: note: no Unofficial_Patch overlay in the staging tree — deploying vanilla", file=sys.stderr)
    return root


def resolve_source(args):
    if args.from_installer:
        return resolve_from_installer(args.from_installer, args.staging)
    return args.source


# ---------------------------------------------------------------- commands


def cmd_scan(args):
    source = resolve_source(args)
    check_anchor(source)
    manifest, excluded = build_manifest(source)
    check_ustar_paths(manifest)
    per_dir = {top: sum(1 for rel in manifest if rel.startswith(top + "/")) for top in SOURCE_DIRS}
    if args.json:
        print(json.dumps({"source": source, "files": len(manifest),
                          "bytes": sum(size for size, _ in manifest.values()),
                          "excluded": excluded, "per_dir": per_dir}))
    else:
        print(f"source: {source}")
        for top in SOURCE_DIRS:
            print(f"  {top}: {per_dir[top]} files")
        print(f"files: {len(manifest)}  bytes: {sum(size for size, _ in manifest.values())}  excluded: {excluded}")
    return 0


def cmd_push(args):
    source = resolve_source(args)
    check_anchor(source)
    if args.required_only:
        manifest = {}
    else:
        manifest, _excluded = build_manifest(source)
    with tempfile.TemporaryDirectory(prefix="vtmb_tables_") as tables_root:
        tables = extract_tables(source, tables_root, find_extractor(args.extractor))
        manifest.update(tables)
        roots = {rel: tables_root for rel in tables}
        return push_manifest(args, source, manifest, roots)


def push_manifest(args, source, manifest, roots):
    check_ustar_paths(manifest)
    preflight_device()
    # Create dest before anything touches it: toybox `df` on a nonexistent path errors
    # (first push on a blank device died here) and the extract `cd` needs it too.
    adb("shell", f"mkdir -p {args.dest}")
    on_device = device_manifest(args.dest)
    changed_rel, _extra = diff_manifests(manifest, on_device)
    changed = [(rel, manifest[rel][0]) for rel in changed_rel]
    push_changed(source, args.dest, changed, args.dry_run, roots)
    if args.dry_run or not changed:
        return 0
    post = device_manifest(args.dest)
    missing, _ = diff_manifests(manifest, post)
    if missing:
        print(f"post-push verify FAILED: {len(missing)} file(s) still differ, e.g. {missing[:5]}", file=sys.stderr)
        return 1
    print("post-push verify OK")

    # KI-074: the engine caches each loose tree's file index at <root>/.vtmb-index so a cold start
    # does not have to enumerate 20k files (~1.9 s on Quest). That cache lists the files that were
    # there when it was written, so a push MUST invalidate it — otherwise the engine keeps serving
    # the old file list and is silently blind to anything this push added. The engine rewrites it on
    # the next launch.
    # check=False on the removal itself: this is cleanup after an ALREADY-VERIFIED push, and aborting
    # a good deploy over it would be wrong. But it is NOT ignorable either — a surviving index means
    # the engine keeps serving the pre-push file list and is silently blind to whatever this push
    # added, which is the one failure mode this cache must never have. So the removal is verified and
    # a survivor is reported loudly rather than assumed gone.
    # KI-074/KI-076: the engine needs MANAGE_EXTERNAL_STORAGE to enumerate /sdcard. A package that
    # lacks it does NOT fail loudly — it reads zero files and reports a 26-second mount of nothing,
    # which reads as a hang. That is exactly what the diy.resource.vtmb rename produced, because the
    # grant was attached to the OLD package name. Granting here means a rename or a fresh install can
    # never silently produce an engine that sees no game data.
    app = args.package if hasattr(args, "package") and args.package else "diy.resource.vtmb"
    grant = adb("shell", f"appops set --uid {app} MANAGE_EXTERNAL_STORAGE allow", check=False)
    if grant.returncode == 0:
        print(f"storage permission granted to {app}")
    else:
        print(f"WARNING: could not grant MANAGE_EXTERNAL_STORAGE to {app}. If the engine reports "
              f"0 files, run: adb shell appops set --uid {app} MANAGE_EXTERNAL_STORAGE allow",
              file=sys.stderr)

    stale = []
    for sub in ("Vampire", "Unofficial_Patch"):
        idx = f"{args.dest}/{sub}/.vtmb-index"
        adb("shell", f"rm -f {idx}", check=False)
        probe = adb("shell", f"ls {idx}", check=False)
        if probe.returncode == 0 and "No such file" not in (probe.stdout + probe.stderr):
            stale.append(idx)
    if stale:
        print(f"WARNING: could not remove {len(stale)} stale loose-index cache(s): {stale}", file=sys.stderr)
        print("         the engine will serve the PRE-PUSH file list until they are deleted by hand.",
              file=sys.stderr)
    else:
        print("stale loose-index caches removed (engine rebuilds them on next launch)")
    return 0


def cmd_verify(args):
    source = resolve_source(args)
    check_anchor(source)
    manifest, _excluded = build_manifest(source)
    preflight_device()
    on_device = device_manifest(args.dest)
    missing, extra = diff_manifests(manifest, on_device)
    mismatch = [rel for rel in missing if rel in on_device]
    absent = [rel for rel in missing if rel not in on_device]
    ok = not missing and not extra
    print(f"verify {args.dest}: {'OK' if ok else 'DIFF'} — "
          f"{len(absent)} missing, {len(mismatch)} differ, {len(extra)} extra")
    for label, rels in (("missing", absent), ("mismatch", mismatch), ("extra", extra)):
        for rel in rels[:10]:
            print(f"  {label}: {rel}")
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(prog="quest_deploy", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name, help_text in (("scan", "inventory the source tree"),
                            ("push", "incrementally deploy to the device"),
                            ("verify", "diff device contents against the source")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--source", default="gamedata")
        p.add_argument("--dest", default=DEFAULT_DEST)
        p.add_argument("--from-installer", nargs="+", metavar="EXE",
                       help="innoextract these GOG installer(s) first and deploy the result")
        p.add_argument("--staging", default=DEFAULT_STAGING)
        if name == "scan":
            p.add_argument("--json", action="store_true")
        if name == "push":
            p.add_argument("--dry-run", action="store_true")
            p.add_argument("--required-only", action="store_true",
                           help="sync only the extracted native tables; leave other game data untouched")
            p.add_argument("--extractor", help="path to vtmb-modconv, which extracts the native tables")
    args = parser.parse_args()
    return {"scan": cmd_scan, "push": cmd_push, "verify": cmd_verify}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
