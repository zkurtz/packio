# packio

Support for writing and reading multiple python objects in a single file. A typical use case is in defining IO methods on a dataclass containing heterogenous data objects, such as a dictionary and a data frame. Example:

TODO

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
