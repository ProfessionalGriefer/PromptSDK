from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class Nested(BaseModel):
    foo: int
    bar: int = 0


class Settings(BaseSettings):
    PROJ_ROOT: Path = Path(__file__).resolve().parents[3]

    hello: str
    nested: Nested
    model_config = SettingsConfigDict(toml_file=["default.toml", "config.custom.toml"])

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls, deep_merge=True),)


class GeneratorSettings(Settings):
    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("tool", "prompt-sdk")
    )
    directories: list[Path]
    use_class: bool = True
    output_path: Path
