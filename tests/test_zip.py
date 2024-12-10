"""Test the zip utilities."""

import zipfile
from pathlib import Path

import pytest

from packio import unzipflat, zipflat


def test_zipflat(tmp_path: Path) -> None:
    """Test the zipflat function."""
    # Create some files to zip.
    file1 = tmp_path / "file1.txt"
    file1.write_text("Hello, world!")
    file2 = tmp_path / "file2.txt"
    file2.write_text("Goodbye, world!")
    # Zip the files.
    zip_path = tmp_path / "archive.zip"
    zipflat(files=[file1, file2], outfile=zip_path)
    # Unzip the files.
    unzip_path = tmp_path / "unzipped"
    unzip_path.mkdir()
    unzipflat(file=zip_path, dest_dir=unzip_path)
    # Check the unzipped files.
    assert (unzip_path / "file1.txt").read_text() == "Hello, world!"
    assert (unzip_path / "file2.txt").read_text() == "Goodbye, world!"


def test_zipflat_duplicate(tmp_path: Path) -> None:
    """Test zipflat with duplicate filenames."""
    # Create some files to zip.
    file1 = tmp_path / "file.txt"
    file1.write_text("Hello, world!")
    file2 = tmp_path / "file.txt"
    file2.write_text("Goodbye, world!")
    # Zip the files.
    zip_path = tmp_path / "archive.zip"
    with pytest.raises(ValueError, match="Filename file.txt is not unique."):
        zipflat(files=[file1, file2], outfile=zip_path)


def test_unzipflat_unflat(tmp_path: Path) -> None:
    """Exception should be raised if unzipped archive has directory structure."""
    # Create a zip archive with a directory structure.
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.writestr("dir/file.txt", "Hello, world!")
    # Try to unzip the file.
    with pytest.raises(ValueError, match="expected a flat archive."):
        unzipflat(file=zip_path, dest_dir=tmp_path)


def test_unzipflat_overwrite(tmp_path: Path) -> None:
    """Test unzipflat with overwrite."""
    # Create a file to zip.
    file = tmp_path / "file.txt"
    file.write_text("Hello, world!")
    # Zip the file.
    zip_path = tmp_path / "archive.zip"
    zipflat(files=[file], outfile=zip_path)
    # Unzip the file.
    unzip_path = tmp_path / "unzipped"
    unzip_path.mkdir()
    unzipflat(file=zip_path, dest_dir=unzip_path)
    # Try to unzip the file again.
    with pytest.raises(FileExistsError, match="file.txt"):
        unzipflat(file=zip_path, dest_dir=unzip_path)


def test_unzipflat_not_zip(tmp_path: Path) -> None:
    """Test unzipflat with a non-zip file."""
    # Create a file to unzip.
    file = tmp_path / "file.txt"
    file.write_text("Hello, world!")
    # Try to unzip the file.
    with pytest.raises(ValueError, match="is not a zip archive."):
        unzipflat(file=file, dest_dir=tmp_path)
