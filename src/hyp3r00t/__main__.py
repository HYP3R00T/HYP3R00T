"""Entry point for the HYP3R00T profile README generator."""

import os
from pathlib import Path

from hyp3r00t.blocks.blog import process_blog
from hyp3r00t.blocks.youtube import process_youtube
from hyp3r00t.config import load_config
from hyp3r00t.readme_generator import merge_blocks, write_readme
from hyp3r00t.template_renderer import create_env, render_block


def _render_raw(instance: dict, base_dir: str) -> str:
    """Render a ``raw`` instance — inline its content directly, no template."""
    path = instance.get("path")
    content = instance.get("content")
    if path:
        full_path = Path(base_dir) / path
        try:
            return full_path.read_text(encoding="utf-8")
        except Exception as e:
            return f"<!-- Error reading {path}: {e} -->"
    if content is not None:
        return content
    return "<!-- No content provided -->"


def main() -> None:
    # The package lives at src/hyp3r00t/, so go up two levels to reach the
    # repo root where hyp3r00t.yaml, content/, assets/ and templates/ live.
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    template_dir = os.path.join(base_dir, "templates")
    output_path = os.path.join(base_dir, "README.md")

    config = load_config(cwd=base_dir)
    order = config.get("order", [])
    instances = config.get("instances", {})

    env = create_env(template_dir)
    rendered_blocks = []

    for instance_id in order:
        instance = instances.get(instance_id)
        if instance is None:
            print(f"⚠️  order references undefined instance '{instance_id}' — skipping")
            continue

        instance_type = instance.get("type")
        try:
            if instance_type == "raw":
                rendered = _render_raw(instance, base_dir)
            elif instance_type == "blog":
                instance["posts"] = process_blog(instance.get("rss_url"), instance.get("max_posts", 5))
                rendered = render_block(env, "blog", instance)
            elif instance_type == "youtube":
                instance["videos"] = process_youtube(instance.get("channel_id"), instance.get("max_videos", 5))
                rendered = render_block(env, "youtube", instance)
            elif instance_type in ("banner", "badges", "social"):
                rendered = render_block(env, instance_type, instance)
            else:
                print(f"⚠️  unknown type '{instance_type}' for instance '{instance_id}' — skipping")
                continue
            rendered_blocks.append(rendered)
        except Exception as e:
            print(f"Error rendering '{instance_id}' ({instance_type}): {e}")

    final_readme = merge_blocks(rendered_blocks)
    write_readme(final_readme, output_path)

    print("✅ README.md generated successfully!")


if __name__ == "__main__":
    main()
