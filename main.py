#!/usr/bin/env python3
"""Sum up 27 November's world news in one image - make.fun entry.

Copies the front-page image held in this repository to entry.png
in the output directory ($MAKEFUN_OUTPUT_DIR, default /output).
"""
import os
import shutil
import sys

IMAGE = "news-20261127.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 8 * 1024 * 1024
MAX_PIXELS = 16_000_000


def check_image(path: str) -> None:
    """Check the held image meets the bounty's limits before copying."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"image is {size} bytes, over the 8 MB limit")
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != PNG_MAGIC or head[12:16] != b"IHDR":
        raise ValueError("image is not a PNG file")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    if width * height > MAX_PIXELS:
        raise ValueError(f"image is {width * height} pixels, over the limit")


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        check_image(src)
        os.makedirs(out_dir, exist_ok=True)
        shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    except (OSError, ValueError) as exc:
        print(f"error: cannot write entry: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
