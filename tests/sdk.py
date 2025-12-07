# AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
from jinja2 import Template
from pathlib import Path


class SDK:
    @staticmethod
    def info_extractor(data: str) -> str:
        template_str = """# Examples

    {{data}}"""
        return Template(template_str).render(data=data)

    @staticmethod
    def test(example: str) -> str:
        """
        Test Markdown file
        """
        template_str = """# This is a test

    You are a very helpful assistant.
    Example:
    {{ example }}"""
        return Template(template_str).render(example=example)


(Path.cwd() / "out.md").write_text(SDK.info_extractor("asdf"))
