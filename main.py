#!/usr/bin/env python3
"""Hand-in entrypoint for The Overnight Edition (news-image-20261122).

The artwork is built locally by draw.py and committed as entry.png.
This entrypoint only copies that committed file into the directory the
grader names through MAKEFUN_OUTPUT_DIR — it never hardcodes a path.
Standard library only.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
