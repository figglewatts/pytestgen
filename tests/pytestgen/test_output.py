from ast import FunctionDef
from os import path

from munch import munchify
from pyfakefs.pytest_plugin import fs
import pytest

from pytestgen.load import PyTestGenInputFile
from pytestgen.parse import PyTestGenParsedSet, PyTestGenParsedFile, get_existing_test_functions
import pytestgen.output

from fixtures import mock_module_testable_func, mock_class_testable_func


@pytest.fixture
def mock_parsed_file(mock_module_testable_func, mock_class_testable_func):
    return PyTestGenParsedFile(
        [mock_module_testable_func(),
         mock_class_testable_func()], PyTestGenInputFile("a_file.py", "a_dir"))


@pytest.fixture
def mock_parsed_set(mock_parsed_file):
    fake_input_set = munchify({"output_dir": "output"})
    return PyTestGenParsedSet([mock_parsed_file], fake_input_set)


def test_output_tests(fs, mock_parsed_set, monkeypatch):
    pytestgen.output.output_tests(mock_parsed_set)
    test_file_path = path.join("output", "a_dir", "test_a_file.py")
    assert path.exists(test_file_path) == True, "test file did not exist"

    # we need to patch FunctionDef back in, it was patched out in the
    # 'mock_class_testable_func' fixture used in 'mock_parsed_set'
    # otherwise isinstance() for FunctionDef will fail in
    # get_existing_test_functions()
    monkeypatch.setattr(pytestgen.parse.ast, "FunctionDef", FunctionDef)

    outputted_funcs = get_existing_test_functions(test_file_path)
    assert outputted_funcs == [
        "test_a_test_function", "test_testclass_a_class_test_function"
    ]


def test_output_tests_include(fs, mock_parsed_set, monkeypatch):
    pytestgen.output.output_tests(mock_parsed_set, include=["a_test_function"])
    test_file_path = path.join("output", "a_dir", "test_a_file.py")
    assert path.exists(test_file_path) == True, "test file did not exist"

    # we need to patch FunctionDef back in, it was patched out in the
    # 'mock_class_testable_func' fixture used in 'mock_parsed_set'
    # otherwise isinstance() for FunctionDef will fail in
    # get_existing_test_functions()
    monkeypatch.setattr(pytestgen.parse.ast, "FunctionDef", FunctionDef)

    outputted_funcs = get_existing_test_functions(test_file_path)
    assert outputted_funcs == ["test_a_test_function"]


def test_output_parsed_file_nonexist(fs, mock_parsed_file, monkeypatch):
    test_file_path = path.join("output", "a_dir", "test_a_file.py")
    pytestgen.output._output_parsed_file(mock_parsed_file, "output")
    assert path.exists(test_file_path) == True, "test file did not exist"

    # we need to patch FunctionDef back in, it was patched out in the
    # 'mock_class_testable_func' fixture used in 'mock_parsed_set'
    # otherwise isinstance() for FunctionDef will fail in
    # get_existing_test_functions()
    monkeypatch.setattr(pytestgen.parse.ast, "FunctionDef", FunctionDef)

    outputted_funcs = get_existing_test_functions(test_file_path)
    assert outputted_funcs == [
        "test_a_test_function", "test_testclass_a_class_test_function"
    ]


def test_output_parsed_file_exists(fs, mock_parsed_file, monkeypatch):
    test_file_path = path.join("output", "a_dir", "test_a_file.py")
    fs.create_file(mock_parsed_file.input_file.get_test_file_path("output"))
    pytestgen.output._output_parsed_file(mock_parsed_file, "output")
    assert path.exists(test_file_path) == True, "test file did not exist"

    # we need to patch FunctionDef back in, it was patched out in the
    # 'mock_class_testable_func' fixture used in 'mock_parsed_set'
    # otherwise isinstance() for FunctionDef will fail in
    # get_existing_test_functions()
    monkeypatch.setattr(pytestgen.parse.ast, "FunctionDef", FunctionDef)

    outputted_funcs = get_existing_test_functions(test_file_path)
    assert outputted_funcs == [
        "test_a_test_function", "test_testclass_a_class_test_function"
    ]


def test_ensure_dir_non_exist(fs):
    pytestgen.output._ensure_dir(path.join("test_dir", "test_name.py"))
    assert path.exists("test_dir") == True


def test_ensure_dir_exist(fs):
    fs.create_dir("test_dir")
    pytestgen.output._ensure_dir(path.join("test_dir", "test_name.py"))
    assert path.exists("test_dir") == True