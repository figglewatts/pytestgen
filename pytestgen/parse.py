"""parse.py

Used for parsing inputs into abstract syntax trees and getting the testable
functions of input files.

What is a testable function? A testable function is a function that is defined
in module or class scope.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
from abc import ABC, abstractmethod
import ast
import logging
from typing import List

from pytestgen import load

# TODO: documentation


class TestableFunc(ABC):
    """TestableFunc is used to store the function def of a function that
    should have a test generated for it.

    Attributes:
        function_def (ast.FunctionDef): The function def of this function.
    """
    @abstractmethod
    def __init__(self, function_def: ast.FunctionDef) -> None:
        self.function_def = function_def

    @abstractmethod
    def get_test_name(self) -> str:
        raise NotImplementedError("Cannot call abstract method")


class ModuleTestableFunc(TestableFunc):
    def __init__(self, function_def: ast.FunctionDef,
                 module: ast.Module) -> None:
        super().__init__(function_def)
        self.module = module

    def get_test_name(self) -> str:
        return f"test_{self.function_def.name.strip('_')}"

    def __repr__(self) -> str:
        return f"ModuleTestableFunc({self.function_def}, {self.module})"


class ClassTestableFunc(TestableFunc):
    def __init__(self, function_def: ast.FunctionDef,
                 class_def: ast.ClassDef) -> None:
        super().__init__(function_def)
        self.class_def = class_def
        self._find_init_function()
        if self.init_function_def is None:
            logging.warning("ClassTestableFunc could not find class __init__()"
                            ", did the class have a constructor?")

    def _find_init_function(self):
        for node in self.class_def.body:
            if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                self.init_function_def = node
                return
        self.init_function_def = None

    def get_test_name(self) -> str:
        class_name = self.class_def.name.lower().strip('_')
        function_name = self.function_def.name.lower().strip('_')
        return f"test_{class_name}_{function_name}"

    def __repr__(self) -> str:
        return f"ClassTestableFunc({self.function_def}, {self.class_def})"


class PyTestGenParsedFile:
    """Used to store the list of testable functions for a given input file.

    Attributes:
        testable_funcs (List[TestableFunc]): The list of testable functions.
        input_file (PyTestGenInputFile): The input file that was parsed.
    """
    def __init__(self, testable_funcs: List[TestableFunc],
                 input_file: load.PyTestGenInputFile) -> None:
        self.testable_funcs = testable_funcs
        self.input_file = input_file

    def __repr__(self) -> str:
        testable_funcs = ", ".join([f.__repr__() for f in self.testable_funcs])
        return f"PyTestGenParsedFile([{testable_funcs}], {self.input_file.__repr__()})"


class PyTestGenParsedSet:
    """Used to store the parsed set of files for a given input set.

    Attributes:
        parsed_files (List[PyTestGenParsedFile]): The list of parsed files.
        input_set (PyTestGenInputSet): The input set used to generate this.
    """
    def __init__(self, parsed_files: List[PyTestGenParsedFile],
                 input_set: load.PyTestGenInputSet) -> None:
        self.parsed_files = parsed_files
        self.input_set = input_set

    def __repr__(self) -> str:
        parsed_files = ", ".join([f.__repr__() for f in self.parsed_files])
        return f"PyTestGenParsedSet([{parsed_files}], {self.input_set.__repr__()})"


def parse_input_set(input_set: load.PyTestGenInputSet) -> PyTestGenParsedSet:
    """Parse the files in an input set to get the testable functions from them.
    """
    parsed_files = []
    for src_file in input_set.input_files:
        parsed_file = _parse_source_file(src_file)
        if len(parsed_file.testable_funcs) == 0:
            continue
        parsed_files.append(parsed_file)
    return PyTestGenParsedSet(parsed_files, input_set)


def get_existing_test_functions(test_file_path: str) -> List[str]:
    """Get the existing test_* functions from a test file."""
    with open(test_file_path, "r") as test_file:
        syntax_tree = ast.parse(test_file.read())
        for node in ast.walk(syntax_tree):
            if isinstance(node, ast.Module):
                # get functions that start with "test_"
                return [
                    fname for fname in _get_module_function_names(node)
                    if fname.startswith("test_")
                ]


def _get_module_function_names(module_node: ast.Module) -> List[str]:
    """For a module node, get a list of the function names defined in the 
    module scope."""
    result = []
    for node in ast.iter_child_nodes(module_node):
        if isinstance(node, ast.FunctionDef):
            result.append(node.name)
    return result


def _parse_source_file(src: load.PyTestGenInputFile) -> PyTestGenParsedFile:
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
            testable_funcs.append(ModuleTestableFunc(node, module_node))
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
            testable_funcs.append(ClassTestableFunc(node, class_node))
    return testable_funcs
