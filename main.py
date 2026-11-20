#!/usr/bin/env python3
"""Copy the pre-rendered front page to the grading output directory.

The image is drawn offline by render.py (Pillow, stdlib-only grading
sandbox cannot draw it), so this entry point only copies bytes and
checks the PNG magic before writing.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != MAGIC:
        sys.exit("entry.png is not a PNG file")
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
