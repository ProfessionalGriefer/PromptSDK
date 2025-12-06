import os
import ast
from jinja2 import Environment, FileSystemLoader, meta
from pathlib import Path

# CONFIGURATION
INPUT_FOLDER = "prompts"  # Folder containing your .md files
OUTPUT_FILE = "prompt_sdk.py"  # The generated Python file


def get_variables_from_template(env, template_name):
    """Parses a Jinja2 template to find undeclared variables."""
    template_source = env.loader.get_source(env, template_name)[0]
    parsed_content = env.parse(template_source)
    # find_undeclared_variables returns a set of variable names found in {{ }}
    return meta.find_undeclared_variables(parsed_content)


def generate_sdk():
    env = Environment(loader=FileSystemLoader(INPUT_FOLDER))

    # Start building the Python file content
    output_code = [
        "# AUTOMATICALLY GENERATED FILE. DO NOT EDIT.",
        "from jinja2 import Template",
        "",
        "class PromptSDK:",
    ]

    # Iterate over all markdown files in the folder
    files = [
        f for f in os.listdir(INPUT_FOLDER) if f.endswith(".md") or f.endswith(".txt")
    ]

    if not files:
        print(f"No templates found in {INPUT_FOLDER}")
        return

    for filename in files:
        function_name = Path(filename).stem
        # Sanitize function name (replace spaces/dashes with underscores)
        function_name = function_name.replace(" ", "_").replace("-", "_")

        # Get variables from the file
        variables = get_variables_from_template(env, filename)
        sorted_vars = sorted(list(variables))

        # Create function arguments string: "name: str, company: str"
        args_str = ", ".join([f"{var}: str" for var in sorted_vars])

        # Create dictionary for the template: "{'name': name, 'company': company}"
        kwargs_str = ", ".join([f"'{var}': {var}" for var in sorted_vars])

        # Read the raw template content to embed it (optional, or load from file at runtime)
        # Here we embed it so the generated file is standalone.
        with open(os.path.join(INPUT_FOLDER, filename), "r") as f:
            raw_content = f.read()

        # Escape triple quotes to prevent syntax errors in the generated string
        raw_content_safe = raw_content.replace('"""', '\\"\\"\\"')

        # Append the function definition
        output_code.append(f"""
    @staticmethod
    def {function_name}({args_str}) -> str:
        \"\"\"
        Generates prompt for: {filename}
        \"\"\"
        template_str = \"\"\"{raw_content_safe}\"\"\"
        return Template(template_str).render({kwargs_str})
""")

    # Write the generated code to file
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(output_code))

    print(f"✅ Generated {OUTPUT_FILE} with {len(files)} functions.")


if __name__ == "__main__":
    generate_sdk()
