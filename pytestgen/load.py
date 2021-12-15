"""input.py

Used for getting/organising inputs to pytestgen.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
from importlib.machinery import FileFinder
import logging
import os
from os import path
import pkgutil
from typing import List


class PyTestGenInputFile:
    """An input source file to have tests generated for.

    Attributes:
        name (str): The filename of the source file.
        path (str): The directory (relative to project dir) of the source file.
        full_path (str): The full path to the input file.
    """
    def __init__(self, name: str, file_path: str) -> None:
        self.name = name
        self.path = path.normpath(file_path)
        self.full_path = path.join(file_path, name)

    def get_module(self) -> str:
        return self.full_path.replace(os.sep, ".")[:-3]

    def get_test_file_path(self, output_dir: str) -> str:
        return path.join(output_dir, self.path,
                         f"test_{self.name[:-3].strip('_')}.py")

    def has_test_file(self, output_dir: str) -> bool:
        return path.exists(self.get_test_file_path(output_dir))

    def __eq__(self, other) -> bool:
        if isinstance(other, PyTestGenInputFile):
            return self.name == other.name and \
                self.path == other.path and \
                self.full_path == other.full_path
        return False

    def __repr__(self) -> str:
        return f"PyTestGenInputFile(\"{self.name}\", \"{self.path}\")"


class PyTestGenInputSet:
    """A set of input files for generating tests from.

    Attributes:
        output_dir (str): The directory to output tests to.
        input_files (List[PyTestGenInputFile]): The files to generate tests for.
    """
    def __init__(self, output_dir: str,
                 input_files: List[PyTestGenInputFile]) -> None:
        self.output_dir = output_dir
        self.input_files = input_files

    def __eq__(self, other) -> bool:
        if isinstance(other, PyTestGenInputSet):
            return self.input_files == other.input_files \
                and self.output_dir == other.output_dir
        return False

    def __repr__(self) -> str:
        input_files = ", ".join([f"{f.__repr__()}" for f in self.input_files])
        return f"PyTestGenInputSet(\"{self.output_dir}\", [ {input_files} ])"


def directory(dir_path: str, output_dir: str) -> PyTestGenInputSet:
    """Create an input set from python files in a directory.

    Args:
        dir_path (str): The path to the directory to use.
        output_dir (str): The path to output tests to.

    Returns:
        PyTestGenInputSet: An input set containing the files.
    """
    input_files = _get_python_files_from_dir(dir_path, output_dir)
    return PyTestGenInputSet(output_dir, input_files)


def filename(file: str, output_dir: str) -> PyTestGenInputSet:
    """Create an input set from a single file.

    Args:
        file (str): The path to the file to use.
        output_dir (str): The path to output tests to.
    
    Returns:
        PyTestGenInputSet: An input set containing the file.

    Raises:
        ValueError: If 'file' did not have .py extension.
    """
    _, ext = path.splitext(file)
    if ext != ".py":
        raise ValueError(f"File '{file}' should have .py extension")

    input_filename = path.basename(file)
    input_dirname = path.dirname(file)
    input_files = [PyTestGenInputFile(input_filename, input_dirname)]
    return PyTestGenInputSet(output_dir, input_files)


def _get_python_files_from_dir(directory_path: str,
                               output_dir: str) -> List[PyTestGenInputFile]:
    """Get all the python files under a directory as input files.

    Args:
        directory (str): The directory to use.
        output_dir (str): The path to output tests in.

    Returns:
        List[PyTestGenInputFile]: The list of input files.
    """
    result = []
    for dir_path, _, file_names in os.walk(directory_path):
        for file_name in [f for f in file_names if f.endswith(".py")]:
            result.append(PyTestGenInputFile(file_name, dir_path))
    return result
