__all__ = ["tempdir", "tempfile"]


import os
from tempfile import mkdtemp, mkstemp


def tempdir():
    """create temp dir and return path"""
    return mkdtemp()


def tempfile():
    """create temp file and return path"""
    f, path = mkstemp()
    os.close(f)
    return path
