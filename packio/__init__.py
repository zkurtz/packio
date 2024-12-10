"""Public methods and classes for packio package."""

from importlib.metadata import version

from packio.io import Reader as Reader
from packio.io import Writer as Writer
from packio.zip import unzipflat as unzipflat
from packio.zip import zipflat as zipflat

__version__ = version("packio")
__all__ = [
    "Reader",
    "Writer",
    "zipflat",
    "unzipflat",
]
