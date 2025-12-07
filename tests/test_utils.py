from prompt_sdk.utils import parse_prompt, sanitize_function_name
from prompt_sdk.models import PromptFrontmatter


def test_parse_prompt():
    test_str = """
---
name: Test
description: Test description
---
Foo
Bar
"""
    content, prompt_frontmatter = parse_prompt(test_str)
    assert content == "Foo\nBar"
    assert prompt_frontmatter == PromptFrontmatter(
        name="Test", description="Test description"
    )


def test_sanitize_function_name():
    filenames = [
        "info extractor.md",
        "info-extractor.md",
        "info_extractor.md",
    ]
    for filename in filenames:
        assert sanitize_function_name(filename) == "info_extractor.md"
