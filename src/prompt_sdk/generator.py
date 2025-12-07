from jinja2.nodes import Template
from prompt_sdk.utils import (
    get_prompt_files,
    sanitize_function_name,
    sanitize_prompt,
    parse_prompt,
)
from prompt_sdk.config import settings
from jinja2 import Environment, FileSystemLoader, meta
from pathlib import Path
import textwrap


def get_file_code() -> list[str]:
    return [
        "# AUTOMATICALLY GENERATED FILE. DO NOT EDIT.",
        "from jinja2 import Template",
        "",
        f"class {settings.class_name}:" if settings.use_class else "",
    ]


def get_function_code(
    function_name: str,
    function_description: str | None,
    args_str: str,
    prompt: str,
    kwargs_str: str,
    use_class: bool,
):
    doc_string = (
        f"""\"\"\"
    {function_description}
    \"\"\""""
        if function_description is not None
        else ""
    )

    function_code = f"""def {function_name}({args_str}) -> str:
    {doc_string}
    template_str = \"\"\"{prompt}\"\"\"
    return Template(template_str).render({kwargs_str})
"""
    if use_class:
        return textwrap.indent(f"@staticmethod\n{function_code}", "    ")
    else:
        return function_code


def get_variables_from_template(env: Environment, template_name: str) -> list[str]:
    """Parses a Jinja2 template to find undeclared variables."""
    template_source: str = env.loader.get_source(env, template_name)[0]
    parsed_content: Template = env.parse(template_source)
    # find_undeclared_variables returns a set of variable names found in {{ }}
    variables = meta.find_undeclared_variables(parsed_content)
    return sorted(list(variables))


def generate_sdk():
    env = Environment(loader=FileSystemLoader(settings.input_path))

    # Start building the Python file content
    output_code: list[str] = get_file_code()
    files = get_prompt_files()

    # Iterate over all markdown files in the folder
    if not files:
        print(f"No templates found in {settings.input_path}")
        return

    for file in files:
        function_name = sanitize_function_name(Path(file).stem)
        variables = get_variables_from_template(env, file.name)

        # Create function arguments string: "name: str, company: str"
        args_str = ", ".join([f"{var}: str" for var in variables])

        # Create dictionary for the template: "{'name': name, 'company': company}"
        kwargs_str = ", ".join([f"{var}={var}" for var in variables])

        file_path = settings.input_path / file.name
        file_content = file_path.read_text()

        prompt, frontmatter = parse_prompt(file_content)

        function_code = get_function_code(
            frontmatter.name or function_name,
            frontmatter.description,
            args_str,
            sanitize_prompt(prompt),
            kwargs_str,
            settings.use_class,
        )
        output_code.append(function_code)

    # Write the generated code to file
    settings.output_path.write_text("\n".join(output_code))

    print(f"Generated {settings.output_path} with {len(files)} functions.")


if __name__ == "__main__":
    generate_sdk()
