import os
import sys


def find_data_file(filename: str):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, "./assets", filename)
