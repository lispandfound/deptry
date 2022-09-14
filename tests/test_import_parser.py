import os
from pathlib import Path

from deptry.import_parser import ImportParser
from deptry.utils import run_within_dir


def test_import_parser_py():
    imported_modules = ImportParser().get_imported_modules_from_file(Path("tests/data/some_imports.py"))
    assert set(imported_modules) == set(["os", "pathlib", "typing", "pandas", "numpy"])


def test_import_parser_ipynb():
    imported_modules = ImportParser().get_imported_modules_from_file(
        Path("tests/data/example_project/src/notebook.ipynb")
    )
    assert set(imported_modules) == set(["click", "urllib3", "toml"])


def test_import_parser_ifelse():
    imported_modules = ImportParser().get_imported_modules_from_str(
        """
x=1
import numpy
if x>0:
    import pandas
elif x<0:
    from typing import List
else:
    import logging
"""
    )
    assert set(imported_modules) == set(["numpy", "pandas", "typing", "logging"])


def test_import_parser_tryexcept():
    imported_modules = ImportParser().get_imported_modules_from_str(
        """
import pandas as pd
from numpy import random
try:
    import click
except:
    import logging
"""
    )
    assert set(imported_modules) == set(["numpy", "pandas", "click", "logging"])


def test_import_parser_func():
    imported_modules = ImportParser().get_imported_modules_from_str(
        """
import pandas as pd
from numpy import random
def func():
    import click
"""
    )
    assert set(imported_modules) == set(["numpy", "pandas", "click"])


def test_import_parser_class():
    imported_modules = ImportParser().get_imported_modules_from_str(
        """
import pandas as pd
from numpy import random
class MyClass:
    def __init__(self):
        import click
"""
    )
    assert set(imported_modules) == set(["numpy", "pandas", "click"])


def test_import_parser_relative():
    imported_modules = ImportParser().get_imported_modules_from_str("""from . import foo\nfrom .foo import bar""")
    assert set(imported_modules) == set([])


def test_import_parser_ignores_setuptools(tmp_path):
    with run_within_dir(tmp_path):
        with open("file.py", "w") as f:
            f.write("import setuptools\nimport foo")
        imported_modules = ImportParser().get_imported_modules_for_list_of_files(["file.py"])
        assert set(imported_modules) == set(["foo"])


def test_import_parser_file_encodings(tmp_path):

    with run_within_dir(tmp_path):
        with open("file1.py", "w", encoding="utf-8") as f:
            f.write(
                """#!/usr/bin/python
# -*- encoding: utf-8 -*-
import foo
print('嘉大')
"""
            )
        with open("file2.py", "w", encoding="iso-8859-15") as f:
            f.write(
                """
#!/usr/bin/python
# -*- encoding: iso-8859-15 -*-
import foo
print('Æ	Ç')
"""
            )
        with open("file3.py", "w", encoding="utf-16") as f:
            f.write(
                """#!/usr/bin/python
# -*- encoding: utf-16 -*-
import foo
print('嘉大')
"""
            )
        with open("file4.py", "w", encoding="cp861") as f:
            f.write(
                """#!/usr/bin/python
# -*- encoding: cp861 -*-
import foo
print('foo')
"""
            )

        imported_modules = ImportParser().get_imported_modules_from_file(Path("file1.py"))
        assert set(imported_modules) == set(["foo"])

        imported_modules = ImportParser().get_imported_modules_from_file(Path("file2.py"))
        assert set(imported_modules) == set(["foo"])

        imported_modules = ImportParser().get_imported_modules_from_file(Path("file3.py"))
        assert set(imported_modules) == set(["foo"])

        imported_modules = ImportParser().get_imported_modules_from_file(Path("file4.py"))
        assert set(imported_modules) == set(["foo"])
