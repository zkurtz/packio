"""Public methods and classes for packio package."""

from importlib.metadata import version

from packio.io import Reader as Reader
from packio.io import Writer as Writer
from packio.zipping import unzip as unzip
from packio.zipping import unzipflat as unzipflat
from packio.zipping import zip as zip
from packio.zipping import zipflat as zipflat

__version__ = version("packio")
__all__ = [
    "Reader",
    "Writer",
    "zip",
    "unzip",
    "zipflat",
    "unzipflat",
]
