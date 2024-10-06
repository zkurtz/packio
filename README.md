# packio

Support for writing and reading multiple python objects in a single file. A typical use case is in defining IO methods on a dataclass containing heterogenous data objects, such as a dictionary and a data frame.

## Example

```
import json
from pathlib import Path
import pandas as pd
from dataclasses import dataclass
from packio import Reader, Writer


@dataclass
class MyData:
    """A simple data class for testing.

    Attributes:
        documentation: Description of what this class is all about.
        df: A data frame.
        lookup: A dictionary.
    """

    documentation: str
    df: pd.Dataframe
    lookup: dict[str, int]

    def save(self, path: Path) -> None:
        """Save the data class to disk."""
        with Writer(path) as writer:
            writer.file("documentation.txt").write_text(self.documentation)
            df.to_parquet(writer.file("df.parquet"))
            with writer.file("lookup.json").open("w") as f:
                json.dump(self.lookup, f)

    @classmethod
    def from_file(cls, path: Path) -> "MyData":
        """Load the data class from disk."""
        with Reader(path) as reader:
            documentation = reader.file("documentation.txt").read_text()
            df = pd.read_parquet(reader.file("df.parquet"))
            with reader.file("lookup.json").open() as f:
                lookup = json.load(f)
        return cls(documentation=documentation, df=df, lookup=lookup)



data = MyData(
    documentation="This is a test.",
    df=pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
    lookup={"a": 1, "b": 2},
)
data.save(tmp_path / "data.mydata")
loaded = MyData.from_file(tmp_path / "data.mydata")
assert loaded.documentation == data.documentation
pd.testing.assert_frame_equal(loaded.df, data.df)
assert loaded.lookup == data.lookup
```

## Development

Install poetry:
```
curl -sSL https://install.python-poetry.org | python3 -
```

Install [pyenv and its virtualenv plugin](https://github.com/pyenv/pyenv-virtualenv). Then:
```
pyenv install 3.12.2
pyenv global 3.12.2
pyenv virtualenv 3.12.2 packio
pyenv activate packio
```

Install this package and its dependencies in your virtual env:
```
poetry install
```

Set up git hooks:
```
pre-commit install
```
