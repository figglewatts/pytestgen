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

from . import output


class PyTestGenInputFile:
    """An input source file to have tests generated for.

    Attributes:
        name (str): The filename of the source file.
        path (str): The path (relative to project dir) of the source file.
        test_name (str): The name of the test file (or None if not generated).
    """
    def __init__(self, name: str, path: str, test_name: str = None) -> None:
        self.name = name
        self.path = path
        self.test_name = test_name


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


def package(package_name: str, output_dir: str) -> PyTestGenInputSet:
    """Create an input set from a python package.

    Args:
        package_name (str): The package name to use.
        output_dir (str): The path to output tests to.

    Returns:
        PyTestGenInputSet: An input set containing the files.
    """
    input_files = _get_python_files_from_package(package_name, output_dir)
    return PyTestGenInputSet(output_dir, input_files)


def filename(file: str, output_dir: str) -> PyTestGenInputSet:
    """Create an input set from a single file.

    Args:
        file (str): The path to the file to use.
        output_dir (str): The path to output tests to.
    
    Returns:
        PyTestGenInputSet: An input set containing the file.
    """
    input_filename = path.basename(file)
    input_dirname = path.dirname(file)
    # check to see if a test file already existed in output_dir
    test_name = output.find_test_file(file, output_dir)
    input_files = [
        PyTestGenInputFile(input_filename, input_dirname, test_name)
    ]
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
            # check to see if a test file already existed in output_dir
            test_name = output.find_test_file(path.join(dir_path, file_name),
                                              output_dir)
            result.append(PyTestGenInputFile(file_name, dir_path, test_name))
    return result


def _get_python_files_from_package(package_name: str, output_dir: str
                                   ) -> List[PyTestGenInputFile]:
    """Get all the python files in a python package as input files.

    Args:
        package_name (str): The python package to get files from.
        output_dir (str): The path to output tests in.

    Returns:
        List[PyTestGenInputFile]: The list of input files.
    """
    result = []
    possible_packages = [(importer, mod_name, is_pkg)
                         for (importer, mod_name,
                              is_pkg) in pkgutil.walk_packages()
                         if mod_name.startswith(package_name)]

    if len(possible_packages) == 0:
        logging.warn(f"Could not find any packages with name: {package_name}")

    for importer, mod_name, _ in possible_packages:
        file_path = importer.find_spec(mod_name).origin

        # check to see if a test file already existed in output_dir
        test_name = output.find_test_file(file_path, output_dir)

        # break the filepath down into name and path
        file_name = path.basename(file_path)
        file_path = path.dirname(file_path)
        result.append(PyTestGenInputFile(file_name, file_path, test_name))
    return result
