from prompt_sdk.validators import PyFile
from pydantic.types import DirectoryPath
from typing import Annotated
import typer

app = typer.Typer()


@app.command(name="Prompt SDK", help="Generate client libraries from prompts.")
def main(
    input_path: Annotated[
        PyFile,
        typer.Argument(help="Input Directory, e.g. templates/"),
    ],
    output_path: Annotated[DirectoryPath, typer.Argument(help="Output Python file")],
):
    return


if __name__ == "__main__":
    app()
