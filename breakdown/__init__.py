# empty package for distributing data properly with setuptools
import os

def pkg_path(path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
