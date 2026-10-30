"""Supported Markdown profiles and their Pandoc reader/writer settings.

Each profile fixes the Pandoc reader used to parse input and the writer used to
emit output. Recording these settings explicitly follows the specification:
the supported syntax profile, Pandoc version and reader/writer options must be
documented for every conversion direction.

每个配置（profile）固定对应的 Pandoc reader 与 writer；这里显式记录设置，
便于在报告与测试中锁定版本与选项，符合规格书要求。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    """A named Markdown dialect profile. 一个受支持的 Markdown 方言配置。"""

    key: str
    reader: str          # Pandoc reader used to parse source Markdown 解析输入用的 reader
    writer: str          # Pandoc writer used to serialise output Markdown 输出用的 writer
    description: str


# The two required profiles for this project. 本项目要求支持的两个方言配置。
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
    """Return the profile for a key, or raise a clear error.

    根据名称返回配置；名称不合法时抛出明确错误，便于 CLI 与测试定位问题。
    """
    if key not in PROFILES:
        raise ValueError(
            f"Unknown profile '{key}'. Supported profiles: {', '.join(PROFILES)}."
        )
    return PROFILES[key]


def supported_profiles() -> list[str]:
    """List supported profile keys. 返回受支持配置名称列表。"""
    return list(PROFILES.keys())
