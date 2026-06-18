"""Configuration models for the HYP3R00T profile README generator.

Each block instance in ``hyp3r00t.yaml`` declares its type via a ``type:`` field.
Pydantic discriminates over that field via ``Field(discriminator="type")`` so
each instance is validated against the right model at load time.

Adding a new block type = add a Pydantic class below + add it to the ``Instance``
union. No other code changes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from utilityhub_config import load_settings

# ---------- instance types (the catalog) ----------


class RawInstance(BaseModel):
    """Static markdown. The most fundamental type — content is read from
    ``path`` or taken inline from ``content`` and inlined into the README."""

    model_config = ConfigDict(extra="ignore")

    type: Literal["raw"] = "raw"
    path: str | None = None
    content: str | None = None


class BannerInstance(BaseModel):
    """Hero image at the top of the README."""

    model_config = ConfigDict(extra="ignore")

    type: Literal["banner"] = "banner"
    image: str
    alt: str


class BadgeItem(BaseModel):
    """One badge inside ``badges.list``."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    url: HttpUrl


class BadgesInstance(BaseModel):
    """A list of Shields.io badges rendered as inline images."""

    model_config = ConfigDict(extra="ignore")

    type: Literal["badges"] = "badges"
    list: list[BadgeItem]


class SocialLink(BaseModel):
    """One social link inside ``social.links``."""

    model_config = ConfigDict(extra="ignore")

    platform: str
    handle: str
    url: HttpUrl
    badge: str | None = None


class SocialInstance(BaseModel):
    """A list of social media profile links."""

    model_config = ConfigDict(extra="ignore")

    type: Literal["social"] = "social"
    links: list[SocialLink]


class BlogInstance(BaseModel):
    """Dynamic block — fetches the latest posts from an RSS feed."""

    model_config = ConfigDict(extra="ignore")

    type: Literal["blog"] = "blog"
    rss_url: HttpUrl
    max_posts: int = Field(default=5, ge=1, le=20)


class YoutubeInstance(BaseModel):
    """Dynamic block — fetches the latest videos from a YouTube channel."""

    model_config = ConfigDict(extra="ignore")

    type: Literal["youtube"] = "youtube"
    channel_id: str
    max_videos: int = Field(default=5, ge=1, le=50)


# ---------- discriminated union ----------


Instance = Annotated[
    RawInstance | BannerInstance | BadgesInstance | SocialInstance | BlogInstance | YoutubeInstance,
    Field(discriminator="type"),
]


class Config(BaseModel):
    """Top-level config.

    ``order`` is the sequence of instance IDs as they appear in the README.
    ``instances`` maps each ID to its typed instance. Each instance declares
    its type via the discriminator field."""

    model_config = ConfigDict(extra="ignore")

    order: list[str] = Field(default_factory=list)
    instances: dict[str, Instance] = Field(default_factory=dict)


# ---------- loader ----------


def load_config(cwd: Path | str) -> dict[str, Any]:
    """Load and validate ``hyp3r00t.yaml`` via utilityhub_config auto-discovery.

    With ``app_name="hyp3r00t"`` the resolver looks for ``hyp3r00t.toml`` or
    ``hyp3r00t.yaml`` at ``cwd``. Env vars prefixed with ``HYP3R00T_`` override
    any value (e.g. ``HYP3R00T_INSTANCES__PERSONAL_BLOG__MAX_POSTS=3``).

    Returns a plain dict:
        {"order": [...], "instances": {id: {...}, ...}}
    HTTP URLs are coerced to strings so Jinja can render them.
    """
    instance, _metadata = load_settings(
        Config,
        app_name="hyp3r00t",
        cwd=Path(cwd),
        env_prefix="HYP3R00T",
    )
    return instance.model_dump(mode="json")
