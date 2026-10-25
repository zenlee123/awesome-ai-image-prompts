#!/usr/bin/env python3
"""Generate preview images for every prompt in prompts.json via RouterBase.

Usage:
    ROUTERBASE_API_KEY=sk-rb-... python3 scripts/generate.py [--only id1,id2] [--force]

Images are saved to images/<id>.webp (resized to 768px wide with ffmpeg).
Existing images are skipped unless --force is given.
"""
import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://routerbase.com/v1/images/generations"
RAW = "https://raw.githubusercontent.com/zenlee123/awesome-ai-image-prompts/main/images"
POLL_INTERVAL = 4
TIMEOUT = 600
WIDTH = 768


def request(method, url, key, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "awesome-ai-image-prompts",
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())


def result_url(task):
    for item in task.get("data") or []:
        if item.get("url"):
            return item["url"]
    for url in task.get("result_urls") or []:
        return url
    return None


def generate(item, key, out):
    body = {"model": item["model"], "prompt": item["prompt"]["en"],
            "aspect_ratio": item.get("aspect_ratio", "1:1")}
    if item.get("input"):
        # Edit prompts take an existing preview (already pushed to GitHub) as the source image
        body["image_urls"] = [f"{RAW}/{item['input']}.webp"]
    task = request("POST", API, key, body)
    deadline = time.time() + TIMEOUT
    while not result_url(task):
        if task.get("status") == "failed":
            raise RuntimeError(task.get("error_message") or task.get("error") or task)
        if time.time() > deadline:
            raise TimeoutError(task["id"])
        time.sleep(POLL_INTERVAL)
        task = request("GET", f"{API}/{task['id']}", key)

    with tempfile.NamedTemporaryFile(suffix=".img") as tmp:
        req = urllib.request.Request(result_url(task), headers={"User-Agent": "awesome-ai-image-prompts"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            tmp.write(resp.read())
        tmp.flush()
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp.name,
                        "-vf", f"scale='min({WIDTH},iw)':-2", "-quality", "82", str(out)],
                       check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="comma-separated prompt ids")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    key = os.environ.get("ROUTERBASE_API_KEY")
    if not key:
        sys.exit("ROUTERBASE_API_KEY is not set")

    items = json.loads((ROOT / "prompts.json").read_text())["prompts"]
    if args.only:
        wanted = set(args.only.split(","))
        items = [i for i in items if i["id"] in wanted]

    jobs = []
    for item in items:
        out = ROOT / "images" / f"{item['id']}.webp"
        if out.exists() and not args.force:
            continue
        jobs.append((item, out))

    print(f"{len(jobs)} image(s) to generate")
    failed = []
    with concurrent.futures.ThreadPoolExecutor(args.workers) as pool:
        futures = {pool.submit(generate, item, key, out): item["id"] for item, out in jobs}
        for fut in concurrent.futures.as_completed(futures):
            pid = futures[fut]
            try:
                fut.result()
                print(f"  ok   {pid}")
            except Exception as e:
                failed.append(pid)
                print(f"  FAIL {pid}: {e}")
    if failed:
        sys.exit(f"failed: {','.join(failed)}")


if __name__ == "__main__":
    main()
