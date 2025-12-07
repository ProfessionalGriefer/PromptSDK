from pathlib import Path

import frontmatter
from jinja2 import Environment, meta
from jinja2.nodes import Template

from prompt_sdk.models import PromptFrontmatter


def get_variables_from_template(env: Environment, template_name: str) -> list[str]:
    """Parses a Jinja2 template to find undeclared variables."""
    if env.loader is None:
        raise ValueError("The Jinja2 Environment does not have a loader configured.")

    template_source: str = env.loader.get_source(env, template_name)[0]
    parsed_content: Template = env.parse(template_source)
    # find_undeclared_variables returns a set of variable names found in {{ }}
    variables = meta.find_undeclared_variables(parsed_content)
    return sorted(list(variables))


def sanitize_function_name(name: str) -> str:
    return name.replace(" ", "_").replace("-", "_")


def sanitize_prompt(prompt: str) -> str:
    return prompt.replace('"""', '\\"\\"\\"')


def get_prompt_files(input_path: Path):
    SUPPORTED_EXTENSIONS = [".md"]
    return [
        file for file in input_path.glob("*") if file.suffix in SUPPORTED_EXTENSIONS
    ]


def parse_prompt(prompt: str) -> tuple[str, PromptFrontmatter]:
    """
    Returns:
        tuple: (raw_cleaned_content, validated_frontmatter_object)
    """
    # Load parses the YAML and separates the content
    metadata, content = frontmatter.parse(prompt)

    # Validation step: converts dict to Pydantic object
    meta_obj = PromptFrontmatter(**metadata)  # type: ignore

    # post.content is the text *without* the frontmatter
    return content.strip(), meta_obj
