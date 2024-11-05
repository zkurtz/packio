# packio

Packio allows you to use a single file to store and retrieve multiple python objects. A typical use case is to define IO methods on an instance of a class that contains multiple types of objects, such as a
- dictionary
- data frame
- string
- trained ML model (for example, lightgbm and xgboost each have built-in serialization methods for trained models)

When a class contains multiple of these data types, or even multiple instances of the same data type, saving and loading the data associated with a class tends to become unwieldy, requiring the user to either keep track multiple file paths or to fall back to using pickle, which introduces other problems (see below). The goal of packio is to make it as easy as possible to write `save` and `load` methods for such a class while allowing you to keep using all of your favorite object-type-specific serializers (i.e. `to_parquet` for pandas, `json` for dictionaries, `pathlib.Path.write_text` for strings, etc).


## Why not pickle?

The most common approach for serialization of such complex python objects is to use `pickle`. There are many reasons do dislike pickle. As summarized by Gemini, "Python's pickle module, while convenient, has drawbacks. It poses security risks due to potential code execution vulnerabilities when handling untrusted data. Compatibility issues arise because it's Python-specific and version-dependent.  Maintaining pickle can be challenging due to refactoring difficulties and complex debugging." See also [Ben Frederickson](https://www.benfrederickson.com/dont-pickle-your-data/).

## Example

Here is a toy example of a data class with `save` and `from_file` methods powered by `packio`:

```
from dataclasses import dataclass
import json
from pathlib import Path
import pandas as pd
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


# Create an instance of the class, save it, and re-load it as a new instance:
data = MyData(
    documentation="This is an example.",
    df=pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
    lookup={"a": 1, "b": 2},
)
data.save(tmp_path / "data.mydata")
loaded = MyData.from_file(tmp_path / "data.mydata")

# Check that the new class instance matches the old one, at least in terms of it's data attributes:
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
poetry install --with dev
```

Set up git hooks:
```
pre-commit install
```
