from prompt_sdk.config import settings
from prompt_sdk.models import PromptFrontmatter
import frontmatter


def sanitize_function_name(name: str) -> str:
    return name.replace(" ", "_").replace("-", "_")


def sanitize_prompt(prompt: str) -> str:
    return prompt.replace('"""', '\\"\\"\\"')


def get_prompt_files():
    SUPPORTED_EXTENSIONS = [".md"]
    return [
        file
        for file in settings.input_path.glob("*")
        if file.suffix in SUPPORTED_EXTENSIONS
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
