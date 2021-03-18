# Basic Python Project

## Summary

This is basic project which should be used as a pattern for new python projects.

Project includes:

* [Editorconfig](https://editorconfig.org/) settings
* Basic `.gitignore` settings for work with python in JetBrains IDEs or VSCode
* Basic config for [flake8](https://gitlab.com/pycqa/flake8) linter
* Basic config for [mypy](https://github.com/python/mypy) static type checker
* Basic [Pipfile](https://github.com/pypa/pipenv) with dev level dependencies
* Basic config for [pre-commit ](https://pre-commit.com )

## Start working on

1. Install [pipenv](https://github.com/pypa/pipenv)
2. Create virtual environment and install dev level dependencies:
   `pipenv install --dev`
3. Setup pre-commit hooks:
   `pre-commit install`
4. Setup your IDE/Editor and/or plugins for it to support [flake8](https://gitlab.com/pycqa/flake8), [mypy](https://github.com/python/mypy), [Editorconfig](https://editorconfig.org/)
5. Do not foreget to edit this Readme file
