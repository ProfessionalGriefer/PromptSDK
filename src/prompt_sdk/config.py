from pathlib import Path

from pydantic.types import DirectoryPath
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from pydantic_settings.sources.providers.pyproject import (
    PyprojectTomlConfigSettingsSource,
)

from prompt_sdk.validators import PyFile


class Settings(BaseSettings):
    PROJ_ROOT: Path = Path(__file__).resolve().parents[2]
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
        return (PyprojectTomlConfigSettingsSource(settings_cls),)


class GeneratorSettings(Settings):
    model_config = SettingsConfigDict(
        toml_file="pyproject.toml",
        pyproject_toml_table_header=("tool", "prompt-sdk"),
        extra="ignore",
    )
    input_path: DirectoryPath | None = None
    print("Input path", input_path)
    output_path: PyFile | None = None
    use_class: bool = True
    class_name: str = "SDK"


settings = GeneratorSettings()  # type: ignore
