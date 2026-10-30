"""Diagnostic events and the conversion report (Iteration 1 prototype).

The report records the Pandoc version, source/target profiles, structural
statistics and every diagnostic event. Event levels reserve the categories used
by later iterations: info, fallback, loss and warning.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict


# Event severity levels.
LEVEL_INFO = "info"
LEVEL_FALLBACK = "fallback"
LEVEL_LOSS = "loss"
LEVEL_WARNING = "warning"


@dataclass
class DiagnosticEvent:
    """One recorded diagnostic event."""

    stage: str                                   # Pipeline stage where it occurred
    message: str                                 # Human-readable description
    node_type: str | None = None                 # Pandoc AST node type, if applicable
    policy: str | None = None                    # Policy applied, if any
    level: str = LEVEL_INFO                      # info / fallback / loss / warning


class ConversionReport:
    """Collects metadata, statistics and diagnostic events for one conversion."""

    def __init__(self, source_profile: str, target_profile: str, pandoc_version: str):
        self.source_profile = source_profile
        self.target_profile = target_profile
        self.pandoc_version = pandoc_version
        self.events: list[DiagnosticEvent] = []
        self.statistics: dict[str, int] = {}

    def add(
        self,
        stage: str,
        message: str,
        node_type: str | None = None,
        policy: str | None = None,
        level: str = LEVEL_INFO,
    ) -> None:
        """Append a diagnostic event."""
        self.events.append(
            DiagnosticEvent(
                stage=stage,
                message=message,
                node_type=node_type,
                policy=policy,
                level=level,
            )
        )

    def set_statistic(self, name: str, value: int) -> None:
        """Store a structural statistic, such as the block count."""
        self.statistics[name] = value

    def event_counts(self) -> dict[str, int]:
        """Count events by level."""
        counts: dict[str, int] = {}
        for event in self.events:
            counts[event.level] = counts.get(event.level, 0) + 1
        return counts

    def summary(self) -> dict:
        """Machine-readable report dictionary."""
        return {
            "pandoc_version": self.pandoc_version,
            "source_profile": self.source_profile,
            "target_profile": self.target_profile,
            "statistics": self.statistics,
            "event_counts": self.event_counts(),
            "events": [asdict(event) for event in self.events],
        }

    def to_json(self) -> str:
        """Serialise the report as pretty-printed JSON."""
        return json.dumps(self.summary(), indent=2, ensure_ascii=False)

    def to_text(self) -> str:
        """Human-readable plain-text report."""
        lines = [
            "MarkBridge conversion report",
            f"  Pandoc version : {self.pandoc_version}",
            f"  Source profile: {self.source_profile}",
            f"  Target profile: {self.target_profile}",
            f"  Statistics     : {self.statistics}",
            f"  Event counts   : {self.event_counts()}",
            "  Events:",
        ]
        for event in self.events:
            prefix = f"    [{event.level}]"
            extra = f" ({event.node_type})" if event.node_type else ""
            lines.append(f"{prefix} {event.stage}: {event.message}{extra}")
        return "\n".join(lines)
