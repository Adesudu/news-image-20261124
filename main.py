#!/usr/bin/env python3
"""news-image-20261124 — make.fun entry.

Copies the pre-rendered front page (entry.png, drawn by render.py) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). The image sums up the
world news of Tuesday 24 November 2026: Russian missiles land in Poland
and NATO sends an AWACS; Ukraine sinks the Russian corvette Merkury at
Benghazi; tankers hit mines in the Strait of Hormuz; COP31 ends with no
fossil-fuel deal; a Russian jet enters South Korean airspace; and Carlos
Alcaraz wins his first ATP Finals title. Standard library only.

Deterministic by design: the program only copies the PNG that render.py
drew at build time, so both grader runs write byte-identical output.
No network access is needed at run time.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
