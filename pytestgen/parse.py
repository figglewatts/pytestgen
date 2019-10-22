"""parse.py

Used for parsing inputs into abstract syntax trees and getting the testable
functions of input files.

What is a testable function? A testable function is a function that is defined
in module or class scope.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
import ast
from typing import List

from .input import PyTestGenInputSet, PyTestGenInputFile


class TestableFunc:
    """TestableFunc is used to store the function def of a function that
    should have a test generated for it.

    Attributes:
        function_def (ast.FunctionDef): The function def of this function.
        prefix (str): The prefix to give the test function. Used for scoping.
    """
    def __init__(self, function_def: ast.FunctionDef, prefix: str = None):
        self.function_def = function_def
        self.prefix = prefix

    def get_test_name(self) -> str:
        """Get the test name. Test name is "test_[{prefix}_]{function_name}".
        """
        prefix = self.prefix + "_" if self.prefix else ""
        return f"test_{prefix}{self.function_def.name}"


class PyTestGenParsedFile:
    """Used to store the list of testable functions for a given input file.

    Attributes:
        testable_funcs (List[TestableFunc]): The list of testable functions.
        input_file (PyTestGenInputFile): The input file that was parsed.
    """
    def __init__(self, testable_funcs: List[TestableFunc],
                 input_file: PyTestGenInputFile):
        self.testable_funcs = testable_funcs
        self.input_file = input_file


class PyTestGenParsedSet:
    """Used to store the parsed set of files for a given input set.

    Attributes:
        parsed_files (List[PyTestGenParsedFile]): The list of parsed files.
        input_set (PyTestGenInputSet): The input set used to generate this.
    """
    def __init__(self, parsed_files: List[PyTestGenParsedFile],
                 input_set: PyTestGenInputSet):
        self.parsed_files = parsed_files
        self.input_set = input_set


def parse_input_set(input_set: PyTestGenInputSet) -> PyTestGenParsedSet:
    """Parse the files in an input set to get the testable functions from them.
    """
    parsed_files = []
    for src_file in input_set.input_files:
        parsed_files.append(_parse_source_file(src_file))
    return PyTestGenParsedSet(parsed_files, input_set)


def _parse_source_file(src: PyTestGenInputFile) -> PyTestGenParsedFile:
    """Parse a single source file to get its testable functions."""
    with open(src.full_path, "r") as src_file:
        # parse the file into an AST and get testable functions by iterating
        # through the tree's nodes
        syntax_tree = ast.parse(src_file.read())
        testable_funcs = _get_ast_testable_funcs(syntax_tree)
        return PyTestGenParsedFile(testable_funcs, src)


def _get_ast_testable_funcs(syntax_tree: ast.AST) -> List[TestableFunc]:
    """Get the testable functions from a parsed AST.

    Args:
        syntax_tree (ast.AST): The syntax tree to get functions from.

    Returns:
        List[TestableFunc]: A list of testable functions from the tree.
    """
    # we'll check for functions defined in module scope, as well as class scope
    # this is preferable to just iterating through all FunctionDefs, as some
    # of them might be internal functions, and we might get name overlap from
    # some functions in different scopes -- which would make us overwrite tests
    testable_funcs = []
    for node in ast.walk(syntax_tree):
        if isinstance(node, ast.Module):
            testable_funcs += _get_module_testable_funcs(node)
        elif isinstance(node, ast.ClassDef):
            testable_funcs += _get_class_testable_funcs(node)
    return testable_funcs


def _get_module_testable_funcs(module_node: ast.Module) -> List[TestableFunc]:
    """Get the testable functions declared in module scope.

    Args:
        module_node (ast.Module): The module node found in the AST.

    Returns:
        List[TestableFunc]: A list of testable functions from the tree.
    """
    testable_funcs = []
    for node in ast.iter_child_nodes(module_node):
        if isinstance(node, ast.FunctionDef):
            testable_funcs.append(TestableFunc(node))
    return testable_funcs


def _get_class_testable_funcs(class_node: ast.ClassDef) -> List[TestableFunc]:
    """Get the testable functions declared in class scope.

    Args:
        class_node (ast.ClassDef): The class definition node found in the AST.

    Returns:
        List[TestableFunc]: A list of testable functions from the tree.
    """
    testable_funcs = []
    for node in ast.iter_child_nodes(class_node):
        if isinstance(node, ast.FunctionDef):
            # use the class name as a prefix for the test function name, as
            # there may be module functions with names that overlap with this
            # function name
            testable_funcs.append(
                TestableFunc(node, prefix=class_node.name.lower()))
    return testable_funcs