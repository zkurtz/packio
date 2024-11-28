# packio

Packio allows you to use a single file to store and retrieve multiple python objects. For example:
```
import dummio
import pandas as pd
from packio import Reader, Writer

# define some objects and an output filepath
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
lookup = {"a": 1, "b": 2}
filepath = tmp_path / "data.packio"

# save both objects to the same filepath
with Writer(filepath) as writer:
    df.to_parquet(writer.file("df.parquet"))
    dummio.json.save(lookup, filepath=writer.file("lookup.json"))

# load the objects from the file
with Reader(filepath) as reader:
    df2 = pd.read_parquet(reader.file("df.parquet"))
    lookup2 = dummio.json.load(reader.file("lookup.json"))

assert df.equals(df2)
assert lookup == lookup2
```

[Available on pypi](https://pypi.org/project/packio/): `pip install packio`.

## Why a single file and not a directory?

In a word, *encapsulation*. Copy/move operations with a file are simpler than a directory, especially when it comes to moving data across platforms such as to/from the cloud. A file is also more tamper-resistant - it's typically harder to accidentally modify the contents of a file than it is for someone to add or remove files or subdirectories in a directory.

## Why not pickle?

Although `pickle` may be the most common approach for serialization of complex python objects, there are strong reasons to dislike pickle. As summarized by Gemini, "Python's pickle module, while convenient, has drawbacks. It poses security risks due to potential code execution vulnerabilities when handling untrusted data. Compatibility issues arise because it's Python-specific and version-dependent.  Maintaining pickle can be challenging due to refactoring difficulties and complex debugging." See also [Ben Frederickson](https://www.benfrederickson.com/dont-pickle-your-data/).

## Development

Create and activate a virtual env for dev ops:
```
git clone git@github.com:zkurtz/packio.git
cd packio
pip install uv
uv sync
source .venv/bin/activate
pre-commit install
```
