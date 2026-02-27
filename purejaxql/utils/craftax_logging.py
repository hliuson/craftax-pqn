from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from craftax.craftax.constants import (
    Achievement,
    INTERMEDIATE_ACHIEVEMENTS,
    VERY_ADVANCED_ACHIEVEMENTS,
)


_INTERMEDIATE_ACHIEVEMENTS = set(INTERMEDIATE_ACHIEVEMENTS)
_VERY_ADVANCED_ACHIEVEMENTS = set(VERY_ADVANCED_ACHIEVEMENTS)
_ACHIEVEMENT_DIFFICULTY = {}

for achievement in Achievement:
    if achievement.value <= 24:
        difficulty = "basic"
    elif achievement.value in _INTERMEDIATE_ACHIEVEMENTS:
        difficulty = "intermediate"
    elif achievement.value in _VERY_ADVANCED_ACHIEVEMENTS:
        difficulty = "very_advanced"
    else:
        difficulty = "advanced"
    _ACHIEVEMENT_DIFFICULTY[achievement.name.lower()] = difficulty


def is_raw_achievement_metric(metric_key: str) -> bool:
    return metric_key.startswith("Achievements/") or metric_key.startswith(
        "test/Achievements/"
    )


def is_grouped_achievement_metric(metric_key: str) -> bool:
    return "AchievementsByDifficulty/" in metric_key


def add_grouped_achievement_metrics(metrics: MutableMapping[str, Any]) -> None:
    for key, value in list(metrics.items()):
        if "Achievements/" not in key:
            continue

        prefix, achievement_name = key.split("Achievements/", 1)
        difficulty = _ACHIEVEMENT_DIFFICULTY.get(achievement_name)
        if difficulty is None:
            continue

        metrics[
            f"{prefix}AchievementsByDifficulty/{difficulty}/{achievement_name}"
        ] = value


def drop_raw_achievement_metrics(metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in metrics.items() if not is_raw_achievement_metric(k)}


def drop_all_achievement_metrics(metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {
        k: v
        for k, v in metrics.items()
        if not is_raw_achievement_metric(k) and not is_grouped_achievement_metric(k)
    }
