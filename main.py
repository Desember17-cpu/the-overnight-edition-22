#!/usr/bin/env python3
"""Delivery entry point for THE OVERNIGHT EDITION.

The front page itself is rendered ahead of time by draw.py and stored
beside this file as entry.png. All this program does at hand-in time
is copy that committed PNG into the directory the harness names
through the MAKEFUN_OUTPUT_DIR environment variable, creating the
directory first if it does not exist yet.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
ENV_KEY = "MAKEFUN_OUTPUT_DIR"


def deliver():
    out_dir = os.environ[ENV_KEY]
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    print("copied", SOURCE, "->", target)


if __name__ == "__main__":
    deliver()
