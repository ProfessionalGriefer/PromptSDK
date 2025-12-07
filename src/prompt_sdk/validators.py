from pathlib import Path
from typing import Annotated

import typer
from pydantic.functional_validators import AfterValidator


def validate_input_path(path: Path | None) -> Path:
    if path is None:
        raise typer.BadParameter(
            "Error: Missing input path. Provide it via CLI or pyproject.toml."
        )
    return path


def validate_output_path(path: Path | None) -> Path:
    if path is None:
        raise typer.BadParameter(
            "Error: Missing output path. Provide it via CLI or pyproject.toml."
        )

    if path.suffix != ".py":
        # This raises a clean CLI error instead of a crash
        raise typer.BadParameter("Output file must have a .py extension")
    return path


PyFile = Annotated[Path, AfterValidator(validate_output_path)]
