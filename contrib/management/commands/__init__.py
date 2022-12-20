import sys

PY_VER = sys.version


def open_file(file_dir, mode="r"):
    if PY_VER[0] == "2":
        return open(file_dir, mode)
    return open(file_dir, mode, encoding="utf-8")
