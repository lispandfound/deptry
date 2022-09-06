
# deptry


[![Release](https://img.shields.io/github/v/release/fpgmaas/deptry)](https://img.shields.io/github/v/release/fpgmaas/deptry)
[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/deptry/merge-to-main)](https://img.shields.io/github/workflow/status/fpgmaas/deptry/merge-to-main)
[![Commit activity](https://img.shields.io/github/commit-activity/m/fpgmaas/deptry)](https://img.shields.io/github/commit-activity/m/fpgmaas/deptry)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://fpgmaas.github.io/deptry/)
[![Code style with black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports with isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)
[![License](https://img.shields.io/github/license/fpgmaas/deptry)](https://img.shields.io/github/license/fpgmaas/deptry)

---

_deptry_ is a command line tool to check for unused dependencies in a poetry managed Python project. It does so by scanning the imported modules within all Python files in 
a directory and it's subdirectories, and comparing those to the dependencies listed in `pyproject.toml`. 

## Quickstart

### Installation

_deptry_ can be added to your project with 

```
poetry add --group dev deptry
```

or for older versions of poetry:

```
poetry add --dev deptry
```

### Prerequisites

In order to check for obsolete imports, _deptry_ requires a _pyproject.toml_ file to be present in the directory passed as the first argument, and it requires the corresponding environment to be activated.

### Usage

To scan your project for obsolete imports, run

```sh
deptry .
```

_deptry_ can be configured by using additional command line arguments, or 
by adding a `[tool.deptry]` section in _pyproject.toml_. For more information, see [Usage and Configuration](./usage.md)