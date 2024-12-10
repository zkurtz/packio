"""Tools to simplify zipping and unzipping of files."""

import tempfile
import zipfile
from pathlib import Path
from typing import TypeAlias

PathType: TypeAlias = str | Path


def zipflat(*, files: list[PathType], outfile: PathType) -> None:
    """Zip files into a single archive with no directory structure.

    Args:
        files: List of files to zip.
        outfile: Path to the resulting zip archive.

    Raises:
        ValueError: If the names of the provided files are not unique.
    """
    filepaths = [Path(file) for file in files]
    names = [file.name for file in filepaths]
    if len(names) != len(set(names)):
        for name in set(names):
            if names.count(name) > 1:
                raise ValueError(f"Filename {name} is not unique.")
        # This should not be reachable, but just in case:
        raise ValueError("All files must have unique names.")
    with zipfile.ZipFile(outfile, "w") as zipf:
        for file in filepaths:
            zipf.write(file, arcname=file.name)


def unzip(*, file: PathType, dest_dir: PathType) -> None:
    """Unzip a file into a destination directory.

    Args:
        file: Path to the zip archive.
        dest_dir: Directory to unzip the archive into.
    """
    with zipfile.ZipFile(file, "r") as zipf:
        zipf.extractall(dest_dir)


def unzipflat(*, file: PathType, dest_dir: PathType, overwrite: bool = False) -> None:
    """Unzip a file into a destination directory.

    Args:
        file: Path to the zip archive.
        dest_dir: An existing directory to unzip the archive into.
        overwrite: If True, overwrite any existing files in the destination directory.

    Raises:
        ValueError: If the input file is not a zip archive.
        ValueError: If any contents of the input zip archive are directories -- expect a flat archive.
        FileExistsError: If any files in the archive would overwrite existing files in the destination directory.
    """
    if not zipfile.is_zipfile(file):
        raise ValueError(f"File {file} is not a zip archive.")
    for item in zipfile.ZipFile(file, "r").infolist():
        item_path = Path(item.filename)
        if item_path.parts[0] != item_path.name:
            raise ValueError(
                f"Input zip archive contains directory structure in element {item_path}; expected a flat archive."
            )
    if overwrite:
        unzip(file=file, dest_dir=dest_dir)
    else:
        # unzip files into a temporary directory, then move them to the destination only after
        # verifying that no files will be overwritten:
        with tempfile.TemporaryDirectory() as tempdir:
            unzip(file=file, dest_dir=tempdir)
            for file in Path(tempdir).iterdir():
                target = Path(dest_dir) / file.name
                if target.exists():
                    raise FileExistsError(f"File {target} already exists.")
            for file in Path(tempdir).iterdir():
                file.rename(Path(dest_dir) / file.name)
