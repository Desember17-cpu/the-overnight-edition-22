#!/usr/bin/env python3
"""Hand-in entrypoint for The Overnight Edition (NI22, @desember179).

Copies the committed entry.png into the directory named by the
MAKEFUN_OUTPUT_DIR environment variable (default: /output).
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"delivered {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
