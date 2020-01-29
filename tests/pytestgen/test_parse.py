import pytest

import pytestgen.parse


@pytest.mark.parametrize(
    "input_set,expected",
    [
        # TODO: fill in test data for test_parse_input_set
        # pytest.param(, id="")
    ]
)
def test_parse_input_set(input_set, expected):
    # result = pytestgen.parse.parse_input_set(input_set)
    # assert result == expected
    pass


@pytest.mark.parametrize(
    "test_file_path,expected",
    [
        # TODO: fill in test data for test_get_existing_test_functions
        # pytest.param(, id="")
    ]
)
def test_get_existing_test_functions(test_file_path, expected):
    # result = pytestgen.parse.get_existing_test_functions(test_file_path)
    # assert result == expected
    pass


@pytest.mark.parametrize(
    "module_node,expected",
    [
        # TODO: fill in test data for test_get_module_function_names
        # pytest.param(, id="")
    ]
)
def test_get_module_function_names(module_node, expected):
    # result = pytestgen.parse._get_module_function_names(module_node)
    # assert result == expected
    pass


@pytest.mark.parametrize(
    "src,expected",
    [
        # TODO: fill in test data for test_parse_source_file
        # pytest.param(, id="")
    ]
)
def test_parse_source_file(src, expected):
    # result = pytestgen.parse._parse_source_file(src)
    # assert result == expected
    pass


@pytest.mark.parametrize(
    "syntax_tree,expected",
    [
        # TODO: fill in test data for test_get_ast_testable_funcs
        # pytest.param(, id="")
    ]
)
def test_get_ast_testable_funcs(syntax_tree, expected):
    # result = pytestgen.parse._get_ast_testable_funcs(syntax_tree)
    # assert result == expected
    pass


@pytest.mark.parametrize(
    "module_node,expected",
    [
        # TODO: fill in test data for test_get_module_testable_funcs
        # pytest.param(, id="")
    ]
)
def test_get_module_testable_funcs(module_node, expected):
    # result = pytestgen.parse._get_module_testable_funcs(module_node)
    # assert result == expected
    pass


@pytest.mark.parametrize(
    "class_node,expected",
    [
        # TODO: fill in test data for test_get_class_testable_funcs
        # pytest.param(, id="")
    ]
)
def test_get_class_testable_funcs(class_node, expected):
    # result = pytestgen.parse._get_class_testable_funcs(class_node)
    # assert result == expected
    pass


@pytest.mark.parametrize(
    "expected",
    [
        # TODO: fill in test data for test_this_is_a_new_function
        # pytest.param(id="")
    ]
)
def test_this_is_a_new_function(expected):
    # TODO: create assertions for test_this_is_a_new_function
    # pytestgen.parse.this_is_a_new_function()
    pass


@pytest.mark.parametrize(
    "expected",
    [
        # TODO: fill in test data for test_testablefunc_get_test_name
        # pytest.param(id="")
    ]
)
def test_testablefunc_get_test_name(expected):
    # TODO: write test for test_testablefunc_get_test_name
    # cls_instance = pytestgen.parse.TestableFunc(function_def)
    # result = cls_instance.get_test_name()
    # assert result == expected
    pass


@pytest.mark.parametrize(
    "expected",
    [
        # TODO: fill in test data for test_moduletestablefunc_get_test_name
        # pytest.param(id="")
    ]
)
def test_moduletestablefunc_get_test_name(expected):
    # TODO: write test for test_moduletestablefunc_get_test_name
    # cls_instance = pytestgen.parse.ModuleTestableFunc(function_def, module)
    # result = cls_instance.get_test_name()
    # assert result == expected
    pass


@pytest.mark.parametrize(
    "expected",
    [
        # TODO: fill in test data for test_classtestablefunc_find_init_function
        # pytest.param(id="")
    ]
)
def test_classtestablefunc_find_init_function(expected):
    # TODO: write test for test_classtestablefunc_find_init_function
    # cls_instance = pytestgen.parse.ClassTestableFunc(function_def, class_def)
    # TODO: create assertions for test_classtestablefunc_find_init_function
    # cls_instance._find_init_function()
    pass


@pytest.mark.parametrize(
    "expected",
    [
        # TODO: fill in test data for test_classtestablefunc_get_test_name
        # pytest.param(id="")
    ]
)
def test_classtestablefunc_get_test_name(expected):
    # TODO: write test for test_classtestablefunc_get_test_name
    # cls_instance = pytestgen.parse.ClassTestableFunc(function_def, class_def)
    # result = cls_instance.get_test_name()
    # assert result == expected
    pass