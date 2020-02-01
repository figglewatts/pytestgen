from os.path import sep

from munch import Munch, munchify
import pytest

from pytestgen.load import PyTestGenInputSet, PyTestGenInputFile
from pytestgen.parse import ModuleTestableFunc, ClassTestableFunc
import pytestgen.parse


@pytest.fixture
def mock_input_set():
    def _make_input_set(with_output=False):
        return PyTestGenInputSet(
            f"test_data{sep}output" if with_output else "",
            [PyTestGenInputFile("file_a.py", "test_data")])

    return _make_input_set


@pytest.fixture
def mock_class_testable_func(monkeypatch):
    def make_class_testable_func(has_return=False, patch_functiondef=True):
        fake_function_def = munchify({
            "name":
            "a_class_test_function",
            "args": {
                "args": [{
                    "arg": "a"
                }, {
                    "arg": "b"
                }]
            },
            "returns":
            "a value" if has_return else None
        })
        fake_class_def = munchify({
            "name":
            "TestClass",
            "body": [{
                "name": "__init__",
                "args": {
                    "args": [{
                        "arg": "one"
                    }, {
                        "arg": "two"
                    }]
                }
            }]
        })

        if patch_functiondef:
            # patch ast.FunctionDef to a Munch so our fake FunctionDefs pass the isinstance()
            # check
            monkeypatch.setattr(pytestgen.parse.ast, "FunctionDef", Munch)

        return ClassTestableFunc(fake_function_def, fake_class_def)

    return make_class_testable_func


@pytest.fixture
def mock_module_testable_func():
    def make_module_testable_func(has_return=False):
        fake_function_def = munchify({
            "name":
            "a_test_function",
            "args": {
                "args": [{
                    "arg": "a"
                }, {
                    "arg": "b"
                }]
            },
            "returns":
            "a value" if has_return else None
        })
        return ModuleTestableFunc(fake_function_def, None)

    return make_module_testable_func