from contextlib import nullcontext as does_not_raise
from os.path import sep

import pytest
import pyfakefs
from pyfakefs.pytest_plugin import fs

from pytestgen import load
from pytestgen.load import PyTestGenInputSet, PyTestGenInputFile


def test_directory(fs):
    for f in [
            "dir/" + f for f in ["a.py", "b.py", "c.py", "d.txt", "sub/e.py"]
    ]:
        fs.create_file(f)

    result = load.directory("dir", "output")
    assert result == PyTestGenInputSet("output", [
        PyTestGenInputFile("a.py", f"dir"),
        PyTestGenInputFile("b.py", f"dir"),
        PyTestGenInputFile("c.py", f"dir"),
        PyTestGenInputFile("e.py", f"dir{sep}sub")
    ])


@pytest.mark.parametrize(
    "file,expected,raises",
    [("/dir/a_file.py",
      PyTestGenInputSet(
          "output",
          [PyTestGenInputFile("a_file.py", f"{sep}dir")]), does_not_raise()),
     ("txt_file.txt", None, pytest.raises(ValueError))])
def test_filename(fs, file, expected, raises):
    fs.create_file("/dir/a_file.py")

    with raises:
        result = load.filename(file, "output")
        assert result == expected


def test_get_python_files_from_dir(fs):
    for f in [
            "dir/" + f for f in ["a.py", "b.py", "c.py", "d.txt", "sub/e.py"]
    ]:
        fs.create_file(f)

    result = load._get_python_files_from_dir("dir", "output")
    assert result == [
        PyTestGenInputFile("a.py", f"dir"),
        PyTestGenInputFile("b.py", f"dir"),
        PyTestGenInputFile("c.py", f"dir"),
        PyTestGenInputFile("e.py", f"dir{sep}sub")
    ]


@pytest.mark.parametrize(
    "instance,expected",
    [(PyTestGenInputFile("a.py", f"dir"), "dir.a"),
     (PyTestGenInputFile("b.py", f"dir{sep}sub"), "dir.sub.b")])
def test_pytestgeninputfile_get_module(instance, expected):
    result = instance.get_module()
    assert result == expected


@pytest.mark.parametrize("instance,output_dir,expected",
                         [(PyTestGenInputFile("a.py", "dir"), "output",
                           f"output{sep}dir{sep}test_a.py"),
                          (PyTestGenInputFile("b.py", f"dir{sep}sub"),
                           "output", f"output{sep}dir{sep}sub{sep}test_b.py"),
                          (PyTestGenInputFile("__init__.py", "dir"), "output",
                           f"output{sep}dir{sep}test_init.py")])
def test_pytestgeninputfile_get_test_file_path(instance, output_dir, expected):
    result = instance.get_test_file_path(output_dir)
    assert result == expected


def test_pytestgeninputfile_has_test_file(fs):
    fs.create_file("output/dir/test_b.py")
    instance = PyTestGenInputFile("b.py", "dir")
    assert instance.has_test_file("output") == True


def test_pytestgeninputfile_not_has_test_file(fs):
    instance = PyTestGenInputFile("b.py", "dir")
    assert instance.has_test_file("output") == False