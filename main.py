#!/usr/bin/env python3
"""Hand-in entrypoint — The Overnight Edition, round 3 (news-image-20261122).

The page is rendered locally by draw.py and committed as entry.png.
This entrypoint does one thing: copy that committed file into the output
directory named by the MAKEFUN_OUTPUT_DIR environment variable (falling
back to /output only when the variable is unset). Standard library only.
"""
import os
import shutil
import sys


def deliver():
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    dest = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, dest)
    print("delivered %s (%d bytes)" % (dest, os.path.getsize(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(deliver())
