from pathlib import Path

from jinja2 import Environment, FileSystemLoader, meta
from jinja2.nodes import Template

from prompt_sdk.config import settings
from prompt_sdk.models import TemplateInput
from prompt_sdk.utils import (
    get_prompt_files,
    parse_prompt,
    sanitize_function_name,
    sanitize_prompt,
)


def get_variables_from_template(env: Environment, template_name: str) -> list[str]:
    """Parses a Jinja2 template to find undeclared variables."""
    template_source: str = env.loader.get_source(env, template_name)[0]
    parsed_content: Template = env.parse(template_source)
    # find_undeclared_variables returns a set of variable names found in {{ }}
    variables = meta.find_undeclared_variables(parsed_content)
    return sorted(list(variables))


def generate_sdk():
    input_env = Environment(loader=FileSystemLoader(settings.input_path))
    output_env = Environment(loader=FileSystemLoader(settings.TEMPLATES_DIR))
    sdk_template = output_env.get_template("sdk_template.py.jinja")

    # Start building the Python file content
    files = get_prompt_files()

    # Iterate over all markdown files in the folder
    if not files:
        print(f"No templates found in {settings.input_path}")
        return

    functions: list[TemplateInput] = []

    for file in files:
        function_name = sanitize_function_name(Path(file).stem)
        variables = get_variables_from_template(input_env, file.name)

        file_path = settings.input_path / file.name
        file_content = file_path.read_text()
        prompt, frontmatter = parse_prompt(file_content)

        args_str = ", ".join([f"{var}: str" for var in variables])
        kwargs_str = ", ".join([f"{var}={var}" for var in variables])

        functions.append(
            {
                "name": frontmatter.name or function_name,
                "description": frontmatter.description or "",
                "args": args_str,
                "kwargs": kwargs_str,
                "prompt": sanitize_prompt(prompt),
            }
        )

    rendered_code = sdk_template.render(
        use_class=settings.use_class,
        class_name=settings.class_name,
        functions=functions,
    )
    settings.output_path.write_text(rendered_code)
    print(f"Generated {settings.output_path} with {len(files)} functions.")


if __name__ == "__main__":
    generate_sdk()
