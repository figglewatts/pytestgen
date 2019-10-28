"""output.py

Used for getting/organising outputs for pytestgen.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
import os
from os import path

from pytestgen import parse
from pytestgen import load

from . import generator

UNTESTABLE_FUNCTIONS = ["__init__"]

TEST_FILE_MODULES = ["pytest"]


def output_tests(parsed_set: parse.PyTestGenParsedSet):
    for parsed_file in parsed_set.parsed_files:
        _output_parsed_file(parsed_file, parsed_set.input_set.output_dir)


def _output_parsed_file(parsed_file: parse.PyTestGenParsedFile,
                        output_dir: str):
    # check if we were able to find an existing test file for this src file
    if parsed_file.input_file.has_test_file(output_dir):
        _output_to_existing(parsed_file, output_dir)
    else:
        _output_to_new(parsed_file, output_dir)


def _output_to_existing(parsed_file: parse.PyTestGenParsedFile,
                        output_dir: str):
    test_file_path = parsed_file.input_file.get_test_file_path(output_dir)
    module_name = parsed_file.input_file.get_module()
    existing_functions = parse.get_existing_test_functions(test_file_path)
    tests_to_generate = []
    for testable_func in parsed_file.testable_funcs:
        if testable_func.function_def.name in UNTESTABLE_FUNCTIONS:
            continue

        if testable_func.get_test_name() not in existing_functions:
            tests_to_generate.append(testable_func)

    with open(test_file_path, "a") as test_file:
        for test_func in tests_to_generate:
            test_file.write(
                generator.generate_test_func(test_func, module_name))


def _output_to_new(parsed_file: parse.PyTestGenParsedFile, output_dir: str):
    test_file_path = parsed_file.input_file.get_test_file_path(output_dir)
    module_name = parsed_file.input_file.get_module()
    _ensure_dir(test_file_path)
    with open(test_file_path, "w") as test_file:
        test_file.write(
            generator.generate_test_file(TEST_FILE_MODULES, module_name))

        for testable_func in parsed_file.testable_funcs:
            if testable_func.function_def.name in UNTESTABLE_FUNCTIONS:
                continue

            test_file.write(
                generator.generate_test_func(testable_func, module_name))


def _ensure_dir(file_path: str):
    try:
        os.makedirs(path.dirname(file_path))
    except FileExistsError:
        # already existed
        pass