import os

from blocks.blog import process_blog
from blocks.youtube import process_youtube
from config_loader import load_config
from readme_generator import merge_blocks, write_readme
from template_renderer import create_env, render_block


def main() -> None:
    # Define paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, "config.yaml")
    template_dir = os.path.join(base_dir, "templates")
    output_path = os.path.join(base_dir, "README.md")

    # Load the configuration (order preserved in Python 3.7+)
    config = load_config(config_path)

    # Create a Jinja2 environment
    env = create_env(template_dir)

    rendered_blocks = []

    # Iterate over the blocks in the config in order
    for block, details in config.items():
        try:
            if block == "blog":
                details["posts"] = process_blog(details.get("rss_url"), details.get("max_posts", 5))

            if block == "youtube":
                details["videos"] = process_youtube(details.get("channel_id"), details.get("max_videos", 5))

            rendered_block = render_block(env, block, details)
            rendered_blocks.append(rendered_block)
        except Exception as e:
            print(f"Error rendering block '{block}': {e}")

    # Merge all blocks and write to README.md
    final_readme = merge_blocks(rendered_blocks)
    write_readme(final_readme, output_path)

    print("✅ README.md generated successfully!")


if __name__ == "__main__":
    main()
