from pydantic import BaseModel


class PromptFrontmatter(BaseModel):
    name: str | None = None
    description: str | None = None

    class Config:
        extra = "ignore"  # Ignore extra fields in the YAML
