import logging
from typing import List

from jinja2 import Template

from . import parse

MODULE_TEST_FUNC_TEMPLATE = Template(\
"""


@pytest.mark.parametrize(
    "{% for arg in data.arguments %}{{ arg }},{% endfor %}expected",
    [
        # TODO: fill in test data for {{ data.name }}
        # pytest.param({% for arg in data.arguments %}, {% endfor %}id="")
    ]
)
def {{ data.name }}({% for arg in data.arguments %}{{ arg }}, {% endfor %}expected):
    {% if data.returns -%}
    # result = {{ data.module_path }}.{{ data.src_name }}({% for arg in data.arguments %}{{ arg }}{{ ", " if not loop.last }}{% endfor %})
    # assert result == expected
    {% else -%}
    # TODO: create assertions for {{ data.name }}
    # {{ data.module_path }}.{{ data.src_name }}({% for arg in data.arguments %}{{ arg }}{{ ", " if not loop.last }}{% endfor %})
    {% endif -%}
    pass
""")

CLASS_TEST_FUNC_TEMPLATE = Template(\
"""


@pytest.mark.parametrize(
    "instance,{% for arg in data.arguments %}{{ arg }},{% endfor %}expected",
    [
        # TODO: fill in test data for {{ data.name }}
        # pytest.param({{ data.module_path }}.{{ data.class_name }}({% for arg in data.init_arguments %}{{ arg }}{{", " if not loop.last }}{% endfor %}), {% for arg in data.arguments %}, {% endfor %}expected, id="")
    ]
)
def {{ data.name }}(instance, {% for arg in data.arguments %}{{ arg }}, {% endfor %}expected):
    # TODO: write test for {{ data.name }}
    {% if data.returns -%}
    # result = instance.{{ data.src_name }}({% for arg in data.arguments %}{{ arg }}{{ ", " if not loop.last }}{% endfor %})
    # assert result == expected
    {% else -%}
    # TODO: create assertions for {{ data.name }}
    # instance.{{ data.src_name }}({% for arg in data.arguments %}{{ arg }}{{ ", " if not loop.last }}{% endfor %})
    {% endif -%}
    pass
""")

TEST_FILE_TEMPLATE = Template(\
"""{% for module in modules %}import {{ module }}
{% endfor %}
import {{ test_module }}
""")


def generate_class_func(testable_func: parse.ClassTestableFunc,
                        module_path: str) -> str:
    # don't generate a test if we can't create an instance of the class
    if testable_func.init_function_def is None:
        return ""

    data = {
        "arguments": [
            arg.arg for arg in testable_func.function_def.args.args
            if arg.arg != "self"
        ],
        "name":
        testable_func.get_test_name(),
        "src_name":
        testable_func.function_def.name,
        "module_path":
        module_path,
        "class_name":
        testable_func.class_def.name,
        "init_arguments": [
            arg.arg for arg in testable_func.init_function_def.args.args
            if arg.arg != "self"
        ],
        "returns":
        testable_func.function_def.returns is not None
    }
    return CLASS_TEST_FUNC_TEMPLATE.render(data=data)


def generate_module_func(testable_func: parse.ModuleTestableFunc,
                         module_path: str) -> str:
    data = {
        "arguments": [arg.arg for arg in testable_func.function_def.args.args],
        "name": testable_func.get_test_name(),
        "src_name": testable_func.function_def.name,
        "module_path": module_path,
        "returns": testable_func.function_def.returns is not None
    }
    return MODULE_TEST_FUNC_TEMPLATE.render(data=data)


TESTABLE_FUNC_TEMPLATE_MAP = {
    parse.ClassTestableFunc: generate_class_func,
    parse.ModuleTestableFunc: generate_module_func
}


def generate_test_func(testable_func: parse.TestableFunc,
                       module_path: str) -> str:
    logging.info(
        f"Generating '{testable_func.get_test_name()}' from module '{module_path}'"
    )
    return TESTABLE_FUNC_TEMPLATE_MAP[type(testable_func)](testable_func,
                                                           module_path)


def generate_test_file(modules: List[str], test_module: str) -> str:
    return TEST_FILE_TEMPLATE.render(modules=modules, test_module=test_module)