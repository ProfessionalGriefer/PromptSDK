import os
from src.prompt_sdk import PromptSDK
from jinja2 import Template
from pathlib import Path


def a():
    path: Path = Path.cwd() / "prompts" / "test.md"
    prompt = path.read_text()
    template = Template(prompt)
    result = template.render(a=Path.cwd(), list=list)
    print(result)
    # Result: The template executes the shell command.


def b():
    print(PromptSDK.test(var="asdf"))


if __name__ == "__main__":
    b()
