"""Supported Markdown profiles and their Pandoc reader/writer settings.

Each profile fixes the Pandoc reader used to parse input and the writer used to
emit output. These settings are recorded explicitly so the supported syntax
profile, Pandoc version and reader/writer options can be documented for every
conversion direction.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    """A named Markdown dialect profile."""

    key: str
    reader: str    # Pandoc reader used to parse source Markdown
    writer: str    # Pandoc writer used to serialise output Markdown
    description: str


# The two required profiles for this project.
PROFILES = {
    "commonmark": Profile(
        key="commonmark",
        reader="commonmark",
        writer="commonmark",
        description="Strict CommonMark baseline (no GFM extensions).",
    ),
    "gfm": Profile(
        key="gfm",
        reader="gfm",
        writer="gfm",
        description="GitHub Flavoured Markdown (tables, task lists, strikethrough, autolinks).",
    ),
}


def get_profile(key: str) -> Profile:
    """Return the profile for a key, or raise a clear error."""
    if key not in PROFILES:
        raise ValueError(
            f"Unknown profile '{key}'. Supported profiles: {', '.join(PROFILES)}."
        )
    return PROFILES[key]


def supported_profiles() -> list[str]:
    """List supported profile keys."""
    return list(PROFILES.keys())
