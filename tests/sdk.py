# AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
from jinja2 import Template



def test(var: str) -> str:
    """
    test
    """
    template_str = """---
description: "Test Markdown file"
---
# This is a test

{{ var }}
"""
    return Template(template_str).render(var=var)
