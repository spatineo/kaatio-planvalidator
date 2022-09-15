# Project setup

Copied **.devcontainer** and **.vscode** from [spatineo/python-samples](https://github.com/spatineo/python-samples) and started container.



## [poetry](https://python-poetry.org)

Ref:
- https://python-poetry.org/docs/basic-usage/#project-setup

```bash
$ poetry init \
    --name kaatio_plan_validator \
    --description "KAATIO Plan Validator" \
    --python "^3.10" \
    --license MIT \
    --no-interaction
# Some manual steps because init to a pre-existing project.
$ mkdir $(grep name pyproject.toml | cut -f2 -d '"')
echo "__version__ = \"$(grep version pyproject.toml | cut -f2 -d '"')\"" | tee kaatio_plan_validator/__init__.py
$ touch kaatio_plan_validator/main.py
$ poetry shell
```

Reload window.

### Add dependencies

```bash
poetry add fastapi uvicorn[standard]
# Development dependencies
poetry add -D black flake8 isort pytest
```

## Development Environment

- Open dev container in vscode
- Install recomended extensions
- Open terminal
- Run `poetry install`
- Move to poetry virtual environment `poetry shell`
- Select Interpreter in vscode (in the right bottom corner or Ctrl+Shift+P --> Select Interpreter): ./.venv/bin/python
  - If Interpreter is not showing "Reload window"
- Run tests `pytest`
  - To run single test for example 
    `pytest -k test_model_spatial_plan_raises_error_when_plan_identifier_element_text_is_none`
- Run `python run_server.py`
- Open in browser http://localhost:8000/docs

## Build commands

Build locally `poetry build`

Build container `docker-compose build`

