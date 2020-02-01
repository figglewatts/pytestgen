from munch import munchify, Munch
import pytest

from pytestgen.parse import ClassTestableFunc, ModuleTestableFunc
import pytestgen.generator

from fixtures import mock_class_testable_func, mock_module_testable_func


def test_generate_class_func(mock_class_testable_func):
    result_without_return = pytestgen.generator.generate_class_func(
        mock_class_testable_func(has_return=False), "module")
    assert result_without_return == """


@pytest.mark.parametrize(
    "instance,a,b,expected",
    [
        # TODO: fill in test data for test_testclass_a_class_test_function
        # pytest.param(module.TestClass(one, two), , , expected, id="")
    ]
)
def test_testclass_a_class_test_function(instance, a, b, expected):
    # TODO: write test for test_testclass_a_class_test_function
    # TODO: create assertions for test_testclass_a_class_test_function
    # instance.a_class_test_function(a, b)
    pass"""

    result_with_return = pytestgen.generator.generate_class_func(
        mock_class_testable_func(has_return=True), "module")
    assert result_with_return == """


@pytest.mark.parametrize(
    "instance,a,b,expected",
    [
        # TODO: fill in test data for test_testclass_a_class_test_function
        # pytest.param(module.TestClass(one, two), , , expected, id="")
    ]
)
def test_testclass_a_class_test_function(instance, a, b, expected):
    # TODO: write test for test_testclass_a_class_test_function
    # result = instance.a_class_test_function(a, b)
    # assert result == expected
    pass"""


def test_generate_module_func(mock_module_testable_func):
    result_without_return = pytestgen.generator.generate_module_func(
        mock_module_testable_func(has_return=False), "module")
    assert result_without_return == """


@pytest.mark.parametrize(
    "a,b,expected",
    [
        # TODO: fill in test data for test_a_test_function
        # pytest.param(, , id="")
    ]
)
def test_a_test_function(a, b, expected):
    # TODO: create assertions for test_a_test_function
    # module.a_test_function(a, b)
    pass"""

    result_with_return = pytestgen.generator.generate_module_func(
        mock_module_testable_func(has_return=True), "module")
    assert result_with_return == """


@pytest.mark.parametrize(
    "a,b,expected",
    [
        # TODO: fill in test data for test_a_test_function
        # pytest.param(, , id="")
    ]
)
def test_a_test_function(a, b, expected):
    # result = module.a_test_function(a, b)
    # assert result == expected
    pass"""


def test_generate_test_file():
    result = pytestgen.generator.generate_test_file(["a", "b", "c"],
                                                    "test_module")
    assert result == """import a
import b
import c

import test_module"""