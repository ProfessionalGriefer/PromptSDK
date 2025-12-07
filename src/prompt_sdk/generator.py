from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from prompt_sdk.validators import validate_input_path, validate_output_path
from typing import Annotated
import typer
from prompt_sdk.config import settings
from prompt_sdk.models import TemplateInput
from prompt_sdk.utils import (
    get_prompt_files,
    get_variables_from_template,
    parse_prompt,
    sanitize_function_name,
    sanitize_prompt,
)


app = typer.Typer()


@app.command(name="Prompt SDK", help="Generate client libraries from prompts.")
def generate_sdk(
    input_path: Annotated[
        Path | None,
        typer.Option(
            "--input",
            "-i",
            help="Input Directory, e.g. templates/",
            exists=True,  # Typer checks this
            file_okay=False,  # Must be a directory
            dir_okay=True,
            readable=True,
        ),
    ] = settings.input_path,
    output_path: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Output Python file",
            dir_okay=False,
            writable=True,
        ),
    ] = settings.output_path,
    use_class: Annotated[
        bool,
        typer.Option(
            "--class/--function",
            help="True: Write functions as static methods of a class. False: Write functions directly into the output file.",
        ),
    ] = settings.use_class,
    class_name: Annotated[
        str,
        typer.Option(
            "--name", "-n", help="Name of the generated class when use_class is True."
        ),
    ] = settings.class_name,
):
    input_path = validate_input_path(input_path)
    output_path = validate_output_path(output_path)

    input_env = Environment(loader=FileSystemLoader(input_path))
    output_env = Environment(loader=FileSystemLoader(settings.TEMPLATES_DIR))
    sdk_template = output_env.get_template("sdk_template.py.jinja")

    # Start building the Python file content
    files = get_prompt_files(input_path)

    # Iterate over all markdown files in the folder
    if not files:
        print(f"No templates found in {input_path}")
        return

    functions: list[TemplateInput] = []

    for file in files:
        function_name = Path(file).stem
        variables = get_variables_from_template(input_env, file.name)

        file_path = input_path / file.name
        file_content = file_path.read_text()
        prompt, frontmatter = parse_prompt(file_content)

        args_str = ", ".join([f"{var}: str" for var in variables])
        kwargs_str = ", ".join([f"{var}={var}" for var in variables])

        functions.append(
            {
                "name": sanitize_function_name(frontmatter.name or function_name),
                "description": frontmatter.description or "",
                "args": args_str,
                "kwargs": kwargs_str,
                "prompt": sanitize_prompt(prompt),
            }
        )

    rendered_code = sdk_template.render(
        use_class=use_class,
        class_name=class_name,
        functions=functions,
    )
    output_path.write_text(rendered_code)
    print(f"Generated {output_path} with {len(files)} functions.")


if __name__ == "__main__":
    app()
