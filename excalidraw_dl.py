#!/usr/bin/env python3
"""
excalidraw_dl.py — Download read-only Excalidraw+ presentations as .excalidraw files.

Usage:
    python excalidraw_dl.py <url> [url2 ...] [-o OUTPUT_DIR]

Example:
    python excalidraw_dl.py https://link.excalidraw.com/p/readonly/XXXXX -o ./slides
"""

import argparse
import json
import os
import re
import sys
import urllib.request


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def extract_scene(html: str) -> tuple[str, dict]:
    """Returns (title, scene_dict) from an Excalidraw+ read-only page HTML."""

    # Title
    title_m = re.search(r"<title>([^<]+)</title>", html)
    title = title_m.group(1).replace(" - Excalidraw+", "").strip() if title_m else "scene"

    # Find the Next.js RSC payload chunk containing sceneContents
    idx = html.find('"sceneContents":')
    if idx == -1:
        raise ValueError("No sceneContents found in page. Is this a valid read-only Excalidraw+ link?")

    # Find the start of the push block that contains it
    start = html.rfind("self.__next_f.push", 0, idx)
    chunk = html[start:]
    end = chunk.find("</script>")
    raw = chunk[:end]

    # Strip the push wrapper and unescape
    inner = raw[len('self.__next_f.push([1,"'):]
    inner = inner.rstrip('"\n );')
    decoded = inner.replace('\\"', '"').replace("\\\\", "\\").replace("\\/", "/")

    # Extract the sceneContents JSON object by counting braces
    sc_idx = decoded.find('"sceneContents":')
    rest = decoded[sc_idx + len('"sceneContents":'):]

    depth, end_idx = 0, 0
    for i, c in enumerate(rest):
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break

    if not end_idx:
        raise ValueError("Could not parse scene JSON.")

    scene = json.loads(rest[:end_idx])
    return title, scene


def safe_filename(title: str) -> str:
    return re.sub(r'[/\\:*?"<>|]', "_", title).strip() or "excalidraw-export"


def download(url: str, output_dir: str) -> str:
    print(f"  Fetching  {url}")
    html = fetch_html(url)
    title, scene = extract_scene(html)
    filename = safe_filename(title) + ".excalidraw"
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(scene, f, ensure_ascii=False, indent=2)
    size_kb = os.path.getsize(path) // 1024
    print(f"  Saved     {filename}  ({len(scene['elements'])} elements, {size_kb} KB)")
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Download read-only Excalidraw+ presentations as .excalidraw files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("urls", nargs="+", metavar="URL", help="One or more Excalidraw+ read-only URLs")
    parser.add_argument("-o", "--output", default=".", metavar="DIR", help="Output directory (default: current dir)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    ok, fail = 0, 0
    for url in args.urls:
        try:
            download(url, args.output)
            ok += 1
        except Exception as e:
            print(f"  ERROR     {url}\n            {e}", file=sys.stderr)
            fail += 1

    print(f"\n  Done — {ok} downloaded, {fail} failed.")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
