"""Main tests of packio."""

import dummio
import pandas as pd
from packio import Reader, Writer


def test_io(tmp_path) -> None:
    """Test the dummio package."""
    # define some objects
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    lookup = {"a": 1, "b": 2}

    # save the objects to a single file
    filepath = tmp_path / "data.packio"
    with Writer(filepath) as writer:
        df.to_parquet(writer.file("df.parquet"))
        dummio.json.save(lookup, filepath=writer.file("lookup.json"))

    # load the objects from the file
    with Reader(filepath) as reader:
        df2 = pd.read_parquet(reader.file("df.parquet"))
        lookup2 = dummio.json.load(reader.file("lookup.json"))

    assert df.equals(df2)
    assert lookup == lookup2
