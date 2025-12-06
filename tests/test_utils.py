from prompt_sdk.utils import parse_prompt, PromptFrontmatter


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
