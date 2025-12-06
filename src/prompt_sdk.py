# AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
from jinja2 import Template


class PromptSDK:
    @staticmethod
    def test(var: str) -> str:
        """
        Generates prompt for: test.md
        """
        template_str = """---
description: "Test Markdown file"
---
# This is a test

{{ var }}
"""
        return Template(template_str).render(var=var)
