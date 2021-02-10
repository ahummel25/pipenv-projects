import os
import sys


def find_data_file(filename: str) -> str:
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
        assets_path = "./assets"
    else:
        # The application is not frozen
        datadir = os.path.dirname(__file__)
        assets_path = "../assets"

    return os.path.join(datadir, assets_path, filename)
