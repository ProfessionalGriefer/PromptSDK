from typing import Annotated
from pydantic.functional_validators import AfterValidator
from pathlib import Path

import typer


def validate_py_suffix(path: Path) -> Path:
    if path.suffix != ".py":
        # This raises a clean CLI error instead of a crash
        raise typer.BadParameter("Output file must have a .py extension")
    return path


PyFile = Annotated[Path, AfterValidator(validate_py_suffix)]
