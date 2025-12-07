# PromptSDK

PromptSDK is a CLI tool for generating client code with appropriate type signature from a folder containing prompts in Markdown format.

## Installation

```bash
uv add prompt-sdk-python

uv run promptsdk --help
```

## Explanation

Prompts are often written in Markdown and can get quite long. Writing them directly into your Python function has some disadvantages. It has no syntax highlighting and also bloats up the Python source file.

```py
def format_prompt(doc_texts: str, doc_types_definitions: str):
    return """# Input

The following documents have been uploaded:

{doc_texts}

# Your task

Classify each page in each document into zero or one of the following document types, based on their content:

{doc_types_definitions}
""".format(doc_texts=doc_texts, doc_types_definitions=doc_types_definitions)

agent.run(format_prompt(...))
```

A naive solution would be to write the system prompt in an external Markdown file and read it in the Python code.

```markdown
# Input

The following documents have been uploaded:

{doc_texts}

# Your task

Classify each page in each document into zero or one of the following document types, based on their content:

{doc_types_definitions}
```

```py
prompt_path = PROMPTS_DIR / "classifier.md"
prompt = prompt_path.read_text()

agent.run(prompt.format(...))
```

The problem is that you need to inspect the Markdown file to know which variables are used in the prompt.
PromptSDK solves this by generating client code from a `prompts` folder.

```bash
ls prompts
# info_extractor.md  classifier.md

uv run promptsdk --input prompts --output generated_sdk.py --name SDK
```

```python
from .generated_sdk import SDK

agent.run(SDK.classifier(...))
```

## Prompt Templates

PromptSDK uses [jinja](https://github.com/pallets/jinja) to read the templates.

```markdown
---
name: "classifier"
description: "The text here appears as a docstring in the generated Python code."
---
# Example

PromptSDK finds variables that are enclosed in two curly braces. 
The type of the generated function argument is a String.

{{ example }}
```

## Configuration

PromptSDK looks at `pyproject.toml` for configuration options.
When not given it looks at the CLI flags.

```toml
# pyproject.toml

[tool.prompt-sdk]
input_path = "templates"
output_path = "generated_sdk.py"
use_class = true
class_name = "SDK"
```
