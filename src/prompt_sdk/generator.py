from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from prompt_sdk.validators import PyFile
from pydantic.types import DirectoryPath
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
        PyFile,
        typer.Argument(help="Input Directory, e.g. templates/"),
    ] = settings.input_path,
    output_path: Annotated[
        DirectoryPath, typer.Argument(help="Output Python file")
    ] = settings.output_path,
    use_class: Annotated[
        bool,
        typer.Argument(
            help="True: Write functions as static methods of a class\nFalse: Write functions directly into the file."
        ),
    ] = settings.use_class,
    class_name: Annotated[
        str,
        typer.Argument(
            help="Name of the generated class when use_class is True. Defaults to 'SDK'."
        ),
    ] = settings.class_name,
):
    input_env = Environment(loader=FileSystemLoader(input_path))
    output_env = Environment(loader=FileSystemLoader(settings.TEMPLATES_DIR))
    sdk_template = output_env.get_template("sdk_template.py.jinja")

    # Start building the Python file content
    files = get_prompt_files()

    # Iterate over all markdown files in the folder
    if not files:
        print(f"No templates found in {input_path}")
        return

    functions: list[TemplateInput] = []

    for file in files:
        function_name = sanitize_function_name(Path(file).stem)
        variables = get_variables_from_template(input_env, file.name)

        file_path = input_path / file.name
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
        use_class=use_class,
        class_name=class_name,
        functions=functions,
    )
    output_path.write_text(rendered_code)
    print(f"Generated {output_path} with {len(files)} functions.")


if __name__ == "__main__":
    app()
