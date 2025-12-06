from jinja2.nodes import Template
from prompt_sdk.utils import sanitize_name
from prompt_sdk.config import settings
from jinja2 import Environment, FileSystemLoader, meta
from pathlib import Path


def get_variables_from_template(env: Environment, template_name: str) -> set[str]:
    """Parses a Jinja2 template to find undeclared variables."""
    template_source: str = env.loader.get_source(env, template_name)[0]
    parsed_content: Template = env.parse(template_source)
    # find_undeclared_variables returns a set of variable names found in {{ }}
    return meta.find_undeclared_variables(parsed_content)


def generate_sdk():
    env = Environment(loader=FileSystemLoader(settings.input_path))

    # Start building the Python file content
    output_code = [
        "# AUTOMATICALLY GENERATED FILE. DO NOT EDIT.",
        "from jinja2 import Template",
        "",
        f"class {settings.class_name}:",
    ]

    # Iterate over all markdown files in the folder
    supported_extensions = [".md"]
    files = [
        file
        for file in settings.input_path.glob("*")
        if file.suffix in supported_extensions
    ]

    if not files:
        print(f"No templates found in {settings.input_path}")
        return

    for file in files:
        function_name = sanitize_name(Path(file).stem)

        variables = get_variables_from_template(env, file.name)
        sorted_vars = sorted(list(variables))

        # Create function arguments string: "name: str, company: str"
        args_str = ", ".join([f"{var}: str" for var in sorted_vars])

        # Create dictionary for the template: "{'name': name, 'company': company}"
        kwargs_str = ", ".join([f"{var}={var}" for var in sorted_vars])

        file_path = settings.input_path / file.name
        raw_content = file_path.read_text()

        # Escape triple quotes to prevent syntax errors in the generated string
        raw_content_safe = raw_content.replace('"""', '\\"\\"\\"')

        # Append the function definition
        function_code = (
            f"""
    @staticmethod
    def {function_name}({args_str}) -> str:
        \"\"\"
        Generates prompt for: {file.name}
        \"\"\"
        template_str = \"\"\"{raw_content_safe}\"\"\"
        return Template(template_str).render({kwargs_str})
"""
            if settings.use_class
            else f"""
def {function_name}({args_str}) -> str:
    \"\"\"
    Generates prompt for: {file.name}
    \"\"\"
    template_str = \"\"\"{raw_content_safe}\"\"\"
    return Template(template_str).render({kwargs_str})
"""
        )
        output_code.append(function_code)

    # Write the generated code to file
    settings.output_path.write_text("\n".join(output_code))

    print(f"Generated {settings.output_path} with {len(files)} functions.")


if __name__ == "__main__":
    generate_sdk()
