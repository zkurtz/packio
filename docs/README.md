# Docs dev tips

To update the requirements file for the docs, run the following command from root:

```
uv pip freeze | grep -v "^-e " > docs/requirements.txt && echo "-e ." >> docs/requirements.txt
```

# Dev build

```
sphinx-build -b html -a . _build/html
```
