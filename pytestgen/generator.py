from typing import List

from jinja2 import Template

from . import parse

TEST_FUNC_TEMPLATE = Template(\
"""


@pytest.mark.parametrize(
    "{% for arg in data.arguments %}{{ arg }},{% endfor %}expected",
    [
        # TODO: fill in test data for {{ data.module_path }}.{{ data.src_name }}
        pytest.param({% for arg in data.arguments %}, {% endfor %}id="")
    ]
)
def {{ data.name }}({% for arg in data.arguments %}{{ arg }}, {% endfor %}expected):
    result = {{ data.module_path }}.{{ data.src_name }}({% for arg in data.arguments -%}
            {{ arg }}{{ ", " if not loop.last }}
        {%- endfor %})
    assert result == expected
""")

TEST_FILE_TEMPLATE = Template(\
"""{% for module in modules %}import {{ module }}
{% endfor %}
import {{ test_module }}
""")


def generate_test_func(testable_func: parse.TestableFunc,
                       module_path: str) -> str:
    data = {
        "arguments": [arg.arg for arg in testable_func.function_def.args.args],
        "name": testable_func.get_test_name(),
        "src_name": testable_func.function_def.name,
        "module_path": module_path
    }
    return TEST_FUNC_TEMPLATE.render(data=data)


def generate_test_file(modules: List[str], test_module: str) -> str:
    return TEST_FILE_TEMPLATE.render(modules=modules, test_module=test_module)