from prompt_sdk.config import settings


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
