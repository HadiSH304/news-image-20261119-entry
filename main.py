"""Entry program for make.fun news-image-20261119.

Copies the pre-rendered front-page image (image.jpg, next to this file)
to /output/entry.png. Deterministic: identical bytes on every run.
Standard library only; no network access.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs("/output", exist_ok=True)
    src = os.path.join(HERE, "image.jpg")
    dst = "/output/entry.png"
    with open(src, "rb") as f_in, open(dst, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


if __name__ == "__main__":
    main()
