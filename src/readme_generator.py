def merge_blocks(blocks: list) -> str:
    """
    Merge a list of rendered blocks into one final string.
    """
    return "\n".join(blocks)


def write_readme(content: str, output_path: str) -> None:
    """
    Write the merged content to the README file.
    """
    with open(output_path, "w") as file:
        file.write(content)
