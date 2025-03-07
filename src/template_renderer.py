from jinja2 import Environment, FileSystemLoader


def read_custom_file(path: str) -> str:
    """
    Reads the content of the specified Markdown file.
    Returns the file content as a string.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"<!-- Error reading file at {path}: {e} -->"


def create_env(template_dir: str) -> Environment:
    """
    Create a Jinja2 environment using the given template directory
    and registers the read_custom_file helper for use in templates.
    """
    env = Environment(loader=FileSystemLoader(template_dir))
    env.globals["read_custom_file"] = read_custom_file
    return env


def render_block(env: Environment, block: str, details: dict) -> str:
    """
    Render a specific block using its corresponding template.
    """
    template = env.get_template(f"{block}.md")
    return template.render(details)
