"""Main tests of packio."""

import json
from dataclasses import dataclass
from pathlib import Path

from packio import Reader, Writer


@dataclass
class MyData:
    """A simple data class for testing.

    Attributes:
        documentation: Description of what this class is all about.
        lookup: A dictionary.
    """

    documentation: str
    lookup: dict[str, int]

    def save(self, path: Path) -> None:
        """Save the data class to disk."""
        with Writer(path) as writer:
            writer.file("documentation.txt").write_text(self.documentation)
            with writer.file("lookup.json").open("w") as f:
                json.dump(self.lookup, f)

    @classmethod
    def from_file(cls, path: Path) -> "MyData":
        """Load the data class from disk."""
        with Reader(path) as reader:
            documentation = reader.file("documentation.txt").read_text()
            with reader.file("lookup.json").open() as f:
                lookup = json.load(f)
        return cls(documentation=documentation, lookup=lookup)


def test_packio(tmp_path):
    """Test the packio package."""
    data = MyData(
        documentation="This is a test.",
        lookup={"a": 1, "b": 2},
    )
    data.save(tmp_path / "data.mydata")
    loaded = MyData.from_file(tmp_path / "data.mydata")
    assert loaded.documentation == data.documentation
    assert loaded.lookup == data.lookup
