import pytest

import example


@pytest.mark.parametrize(
    "arg_one,arg_two,expected",
    [
        # TODO: fill in test data for test_testable_func
        # pytest.param(, , id="")
    ]
)
def test_testable_func(arg_one, arg_two, expected):
    # TODO: create assertions for test_testable_func
    # example.testable_func(arg_one, arg_two)
    pass


@pytest.mark.parametrize(
    "instance,an_arg,expected",
    [
        # TODO: fill in test data for test_aclass_testable_func_in_class
        # pytest.param(example.AClass(some, constructor, params), , expected, id="")
    ]
)
def test_aclass_testable_func_in_class(instance, an_arg, expected):
    # TODO: write test for test_aclass_testable_func_in_class
    # TODO: create assertions for test_aclass_testable_func_in_class
    # instance.testable_func_in_class(an_arg)
    pass