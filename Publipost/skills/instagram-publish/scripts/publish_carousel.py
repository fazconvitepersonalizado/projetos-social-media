"""
Publish an Instagram carousel using the Meta Graph API.

Usage:
  python publish_carousel.py --slides-dir conteudos/2026-05-14-slug/slides --caption "caption text"
  python publish_carousel.py --slides-dir conteudos/2026-05-14-slug/slides --caption "text" --dry-run
"""

import argparse
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

API_VERSION = "v25.0"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}"
MAX_SLIDES = 10
POLL_RETRIES = 5
POLL_INTERVAL = 60  # seconds — Meta recommends 1x/min for up to 5 min


def load_credentials() -> tuple[str, str]:
    load_dotenv()
    account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    if not account_id or not token:
        print("ERROR: Missing credentials in .env")
        print("  Required: INSTAGRAM_ACCOUNT_ID and INSTAGRAM_ACCESS_TOKEN")
        sys.exit(1)
    return account_id, token


# ---------------------------------------------------------------------------
# Image hosting
# ---------------------------------------------------------------------------

def upload_to_catbox(file_path: Path) -> str:
    print(f"  Uploading {file_path.name} to catbox.moe...")
    with open(file_path, "rb") as f:
        r = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload", "userhash": ""},
            files={"fileToUpload": f},
            timeout=60,
        )
    r.raise_for_status()
    url = r.text.strip()
    if not url.startswith("http"):
        print(f"ERROR: catbox.moe returned unexpected response: {url}")
        sys.exit(1)
    print(f"    → {url}")
    return url


# ---------------------------------------------------------------------------
# Meta Graph API helpers
# ---------------------------------------------------------------------------

def api_post(path: str, params: dict) -> dict:
    url = f"{BASE_URL}/{path}"
    r = requests.post(url, params=params, timeout=30)
    data = r.json()
    if "error" in data:
        err = data["error"]
        print(f"ERROR {err.get('code')}: {err.get('message')}")
        if err.get("code") == 190:
            print("  → Token expired. Refresh it at: https://developers.facebook.com/tools/explorer/")
        sys.exit(1)
    return data


def api_get(path: str, params: dict) -> dict:
    url = f"{BASE_URL}/{path}"
    r = requests.get(url, params=params, timeout=30)
    data = r.json()
    if "error" in data:
        err = data["error"]
        print(f"ERROR {err.get('code')}: {err.get('message')}")
        sys.exit(1)
    return data


def create_item_container(account_id: str, token: str, image_url: str) -> str:
    data = api_post(f"{account_id}/media", {
        "image_url": image_url,
        "is_carousel_item": "true",
        "access_token": token,
    })
    return data["id"]


def wait_for_container(token: str, container_id: str) -> None:
    for attempt in range(POLL_RETRIES):
        data = api_get(container_id, {"fields": "status_code", "access_token": token})
        status = data.get("status_code", "UNKNOWN")
        if status == "FINISHED":
            return
        if status == "ERROR":
            print(f"ERROR: Container {container_id} failed with status ERROR")
            sys.exit(1)
        if status == "EXPIRED":
            print(f"ERROR: Container {container_id} expired (24h limit). Create a new container.")
            sys.exit(1)
        print(f"  Container {container_id}: {status} — waiting {POLL_INTERVAL}s...")
        time.sleep(POLL_INTERVAL)
    print(f"ERROR: Container {container_id} did not finish after {POLL_RETRIES} attempts")
    sys.exit(1)


def create_carousel_container(account_id: str, token: str, children: list[str], caption: str) -> str:
    data = api_post(f"{account_id}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(children),
        "caption": caption,
        "access_token": token,
    })
    return data["id"]


def publish_container(account_id: str, token: str, creation_id: str) -> str:
    data = api_post(f"{account_id}/media_publish", {
        "creation_id": creation_id,
        "access_token": token,
    })
    return data["id"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Publish Instagram carousel via Meta API")
    parser.add_argument("--slides-dir", required=True, help="Path to folder containing slide_1.png, slide_2.png, …")
    parser.add_argument("--caption", required=True, help="Caption for the Instagram post")
    parser.add_argument("--dry-run", action="store_true", help="Validate credentials and count slides without publishing")
    args = parser.parse_args()

    slides_dir = Path(args.slides_dir)
    if not slides_dir.exists():
        print(f"ERROR: Slides directory not found: {slides_dir}")
        sys.exit(1)

    slides = sorted(slides_dir.glob("slide_*.png"), key=lambda p: int(p.stem.split("_")[1]))
    if not slides:
        print(f"ERROR: No slide_N.png files found in {slides_dir}")
        sys.exit(1)
    if len(slides) > MAX_SLIDES:
        print(f"ERROR: Instagram supports max {MAX_SLIDES} slides per carousel. Found {len(slides)}.")
        sys.exit(1)

    print(f"Found {len(slides)} slides in {slides_dir}")

    account_id, token = load_credentials()
    print(f"Account ID: {account_id}")

    if args.dry_run:
        print("\n[DRY-RUN] Validating token...")
        data = api_get("me", {"fields": "id,name", "access_token": token})
        print(f"[DRY-RUN] Token valid. Connected as: {data.get('name', data.get('id'))}")
        print(f"[DRY-RUN] Would publish {len(slides)} slides with caption: {args.caption[:60]}...")
        print("[DRY-RUN] All checks passed. Run without --dry-run to publish.")
        return

    # 1. Upload all slides to catbox.moe
    print("\n--- Uploading images ---")
    image_urls = [upload_to_catbox(slide) for slide in slides]

    # 2. Create item containers
    print("\n--- Creating item containers ---")
    container_ids = []
    for i, url in enumerate(image_urls, 1):
        print(f"  Creating container for slide {i}/{len(slides)}...")
        cid = create_item_container(account_id, token, url)
        wait_for_container(token, cid)
        print(f"    → container {cid} ready")
        container_ids.append(cid)

    # 3. Create carousel container
    print("\n--- Creating carousel container ---")
    carousel_id = create_carousel_container(account_id, token, container_ids, args.caption)
    print(f"  Carousel container: {carousel_id}")
    wait_for_container(token, carousel_id)

    # 4. Publish
    print("\n--- Publishing ---")
    post_id = publish_container(account_id, token, carousel_id)
    print(f"\nPublished! Post ID: {post_id}")


if __name__ == "__main__":
    main()
