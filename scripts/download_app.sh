#!/usr/bin/env bash
set -euo pipefail

REPO="saucelabs/sample-app-mobile"
API="https://api.github.com/repos/${REPO}/releases/latest"

echo "Fetching latest release metadata..."
JSON=$(curl -sSL "$API")

mkdir -p apps/android apps/ios

python3 - <<'PY'
import json, os, re, sys, subprocess

data = json.loads(os.environ["JSON"])
assets = data.get("assets", [])

# Heuristics for Sauce sample app names
apk = None
ipa = None

for a in assets:
    name = a.get("name","")
    url = a.get("browser_download_url","")
    lower = name.lower()
    if lower.endswith(".apk") and "android" in lower:
        apk = (name, url)
    if lower.endswith(".ipa") and "ios" in lower:
        ipa = (name, url)

def dl(dest_dir, asset):
    if not asset:
        print(f"Not found for {dest_dir}", file=sys.stderr)
        return
    name, url = asset
    out = os.path.join(dest_dir, name)
    print(f"Downloading {name} -> {out}")
    subprocess.check_call(["curl","-L","-o",out,url])

dl("apps/android", apk)
dl("apps/ios", ipa)
PY
