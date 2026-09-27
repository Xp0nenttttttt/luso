import sys
from pathlib import Path


def asset_path(*parts):
    root = Path(
        getattr(
            sys,
            "_MEIPASS",
            Path(__file__).resolve().parent
        )
    )
    return root.joinpath(*parts)