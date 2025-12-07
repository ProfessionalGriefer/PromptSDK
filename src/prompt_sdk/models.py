from typing import TypedDict
from pydantic import BaseModel


class PromptFrontmatter(BaseModel):
    name: str | None = None
    description: str | None = None

    class Config:
        extra = "ignore"  # Ignore extra fields in the YAML


class TemplateInput(TypedDict):
    name: str
    description: str
    args: str
    kwargs: str
    prompt: str
