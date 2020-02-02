"""output.py

Used for getting/organising outputs for pytestgen.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
import os
from os import path
from typing import List

from pytestgen import parse
from pytestgen import load

from . import generator

UNTESTABLE_FUNCTIONS = ["__init__"]
"""List of functions that we globally shouldn't generate tests for."""

TEST_FILE_MODULES = ["pytest"]
"""List of modules we should import at the top of a generated test file."""


def output_tests(parsed_set: parse.PyTestGenParsedSet,
                 include: List[str] = []) -> None:
    """Output the parsed test files in a parsed set.

    Args:
        parsed_set: The set of parsed files to output.
        include: The list of function names to generate tests for. If empty,
            all functions will be used.
    """
    for parsed_file in parsed_set.parsed_files:
        _output_parsed_file(parsed_file, parsed_set.input_set.output_dir,
                            include)


def _output_parsed_file(parsed_file: parse.PyTestGenParsedFile,
                        output_dir: str,
                        include: List[str] = []) -> None:
    """Output the tests of a parsed file to a directory. Checks to see if a
    test file already existed for the parsed file, and handles not overwriting
    existing tests.

    Args:
        parsed_file: The parsed file to output.
        output_dir: The path to the dir to output test files in.
        include: The list of function names to generate tests for. If empty,
            all functions will be used.
    """
    # check if we were able to find an existing test file for this src file
    if parsed_file.input_file.has_test_file(output_dir):
        _output_to_existing(parsed_file, output_dir, include)
    else:
        _output_to_new(parsed_file, output_dir, include)


def _output_to_existing(parsed_file: parse.PyTestGenParsedFile,
                        output_dir: str,
                        include: List[str] = []) -> None:
    """Output the tests in 'parsed_file' to an existing file, optionally
    only including a whitelist of functions to output tests for. This function
    will ensure tests that already existed in the existing file are not
    overwritten by newly generated tests.

    Args:
        parsed_file: The parsed file to output.
        output_dir: The path to the dir to output test files in.
        include: The list of function names to generate tests for. If empty,
            all functions will be used.
    """
    test_file_path = parsed_file.input_file.get_test_file_path(output_dir)
    module_name = parsed_file.input_file.get_module()
    existing_functions = parse.get_existing_test_functions(test_file_path)
    tests_to_generate = []
    for testable_func in parsed_file.testable_funcs:
        if testable_func.function_def.name in UNTESTABLE_FUNCTIONS:
            continue

        # skip the function if it isn't in the include list (if we have one)
        if any(include) and testable_func.function_def.name not in include:
            continue

        if testable_func.get_test_name() not in existing_functions:
            tests_to_generate.append(testable_func)

    with open(test_file_path, "a", encoding="utf-8") as test_file:
        for test_func in tests_to_generate:
            test_file.write(
                generator.generate_test_func(test_func, module_name))


def _output_to_new(parsed_file: parse.PyTestGenParsedFile,
                   output_dir: str,
                   include: List[str] = []) -> None:
    """Output the tests in 'parsed_file' to an output directory, optionally
    only including a whitelist of functions to output tests for.

    Args:
        parsed_file: The parsed file to output.
        output_dir: The path to the dir to output test files in.
        include: The list of function names to generate tests for. If empty,
            all functions will be used.
    """
    test_file_path = parsed_file.input_file.get_test_file_path(output_dir)
    module_name = parsed_file.input_file.get_module()
    _ensure_dir(test_file_path)
    with open(test_file_path, "w", encoding="utf-8") as test_file:
        test_file.write(
            generator.generate_test_file(TEST_FILE_MODULES, module_name))

        for testable_func in parsed_file.testable_funcs:
            if testable_func.function_def.name in UNTESTABLE_FUNCTIONS:
                continue

            # skip the function if it isn't in the include list (if we have one)
            if any(include) and testable_func.function_def.name not in include:
                continue

            test_file.write(
                generator.generate_test_func(testable_func, module_name))


def _ensure_dir(file_path: str) -> None:
    """Ensures that a directory 'file_path' exists."""
    os.makedirs(path.dirname(file_path), exist_ok=True)