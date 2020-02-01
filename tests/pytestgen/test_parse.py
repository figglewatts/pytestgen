from typing import List

from munch import munchify, Munch
import pytest

import pytestgen.parse
from pytestgen.parse import PyTestGenParsedSet, PyTestGenParsedFile

from fixtures import mock_input_set

TEST_DATA_OUTPUT_PATH = "test_data"


def has_functions(parsed_file: PyTestGenParsedFile,
                  functions: List[str]) -> (bool, str):
    """Checks to see if the parsed file contains a list of functions.

    Args:
        parsed_file: The parsed file.
        functions: The list of functions to check for.

    Returns:
        bool: Whether all the functions were present.
        str: Which functions were missing from the parsed file.
    """
    function_names = [
        func.function_def.name for func in parsed_file.testable_funcs
    ]
    missing = set(functions) - set(function_names)
    return len(missing) == 0, str(missing)


def test_parse_input_set(mock_input_set):
    parsed_set = pytestgen.parse.parse_input_set(mock_input_set())
    result, missing = has_functions(parsed_set.parsed_files[0], [
        "testable_func", "testable_func_with_args", "testable_func_in_class",
        "__init__"
    ])
    assert result == True, f"Missing function(s) in parsed set: {missing}"


def test_get_existing_test_functions(mock_input_set):
    input_set = mock_input_set(with_output=True)
    existing = pytestgen.parse.get_existing_test_functions(
        input_set.input_files[0].get_test_file_path(input_set.output_dir))
    assert existing == [
        "test_testable_func", "test_testable_func_with_args",
        "test_aclass_init", "test_aclass_testable_func_in_class"
    ]


@pytest.mark.parametrize("function_name,expected",
                         [("a_function_name", "test_a_function_name"),
                          ("__init__", "test_init")])
def test_moduletestablefunc_get_test_name(function_name, expected):
    fake_function_def = munchify({"name": function_name})
    cls_instance = pytestgen.parse.ModuleTestableFunc(fake_function_def, None)
    result = cls_instance.get_test_name()
    assert result == expected


@pytest.mark.parametrize("has_init,expected", [(True, "__init__"),
                                               (False, None)])
def test_classtestablefunc_find_init_function(has_init, expected, monkeypatch):
    fake_class_def = munchify({
        "body": [{
            "name": "not an init"
        }, {
            "name": "__init__" if has_init else "__not_init__"
        }]
    })
    # patch ast.FunctionDef to a Munch so our fake FunctionDefs pass the isinstance()
    # check
    monkeypatch.setattr(pytestgen.parse.ast, "FunctionDef", Munch)
    cls_instance = pytestgen.parse.ClassTestableFunc(None, fake_class_def)
    if has_init:
        assert cls_instance.init_function_def.name == expected
    else:
        assert cls_instance.init_function_def == None


@pytest.mark.parametrize(
    "class_name,function_name,expected",
    [("TestClass", "a_test_function", "test_testclass_a_test_function"),
     ("__TestClass__", "a_test_function", "test_testclass_a_test_function"),
     ("TestClass", "__eq__", "test_testclass_eq"),
     ("__TestClass__", "__repr__", "test_testclass_repr")])
def test_classtestablefunc_get_test_name(class_name, function_name, expected):
    fake_class_def = munchify({"name": class_name, "body": []})
    fake_function_def = munchify({"name": function_name})
    cls_instance = pytestgen.parse.ClassTestableFunc(fake_function_def,
                                                     fake_class_def)
    result = cls_instance.get_test_name()
    assert result == expected