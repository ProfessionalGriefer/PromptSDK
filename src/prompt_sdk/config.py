from prompt_sdk.validators import PyFile
from pydantic.types import DirectoryPath
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class Settings(BaseSettings):
    PROJ_ROOT: Path = Path(__file__).resolve().parents[2]
    TEMPLATES_DIR: Path = PROJ_ROOT / "src" / "prompt_sdk" / "templates"
    print(f"Running in Project Root: {PROJ_ROOT}")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


class GeneratorSettings(Settings):
    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("tool", "prompt-sdk")
    )
    input_path: DirectoryPath = Path.cwd() / "tests" / "prompts"
    print(input_path)
    use_class: bool = False
    output_path: PyFile = Path.cwd() / "tests" / "sdk.py"
    class_name: str = "Docs"


settings = GeneratorSettings()  # type: ignore
