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



