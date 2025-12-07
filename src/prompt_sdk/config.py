from pathlib import Path

from pydantic.types import DirectoryPath
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from prompt_sdk.validators import PyFile


class Settings(BaseSettings):
    PROJ_ROOT: Path = Path(__file__).resolve().parents[2]
    TEMPLATES_DIR: Path = PROJ_ROOT / "src" / "prompt_sdk" / "templates"
    # print(f"Running in Project Root: {PROJ_ROOT}")

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
    input_path: DirectoryPath
    use_class: bool = True
    output_path: PyFile
    class_name: str = "SDK"


settings = GeneratorSettings()  # type: ignore
