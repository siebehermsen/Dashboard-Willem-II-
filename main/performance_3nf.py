from __future__ import annotations

from datetime import date
from typing import Dict, Iterable, List, Optional, Tuple

from django.db import transaction

from .models import (
    PerformanceMetric,
    PerformanceMetricType,
    PerformanceSession,
    PerformanceSessionKind,
    Player,
)


TRAINING_CODES = ("total_distance", "hsd", "sprints", "load")
MATCH_CODES = ("accelerations", "decelerations", "hsd", "his", "total_distance", "sprints", "load")
TEST_CODES = ("sprint_10", "sprint_30", "cmj", "squat_jump", "isrt", "submax", "curr_weight", "length", "sum_skinfolds")


def _to_float_or_none(raw):
    if raw in (None, ""):
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def fetch_performance_rows(session_kind: str, player: Optional[Player] = None) -> List[dict]:
    kind_code = (session_kind or "").strip().lower()
    qs = (
        PerformanceSession.objects
        .filter(session_kind_ref__code=kind_code)
        .select_related("player")
        .prefetch_related("metrics__metric_type")
    )
    if player is not None:
        qs = qs.filter(player=player)

    rows: List[dict] = []
    for session in qs:
        metric_map = {m.metric_type.code: m.value for m in session.metrics.all()}
        rows.append(
            {
                "session_id": session.id,
                "player_id": session.player_id,
                "player_name": session.player.name,
                "player_obj": session.player,
                "session_date": session.session_date,
                "week": session.week,
                **metric_map,
            }
        )
    return rows


@transaction.atomic
def upsert_performance_session_metrics(
    *,
    player: Player,
    session_kind: str,
    session_date: date,
    metrics: Dict[str, object],
    week: Optional[int] = None,
    source_tag: str = "app_3nf",
) -> Tuple[PerformanceSession, bool]:
    kind_code = (session_kind or "").strip().lower()
    if not kind_code:
        raise ValueError("session_kind is required")
    label_map = {"training": "Training", "match": "Wedstrijd", "test": "Test"}
    kind_obj, _ = PerformanceSessionKind.objects.get_or_create(
        code=kind_code,
        defaults={"label": label_map.get(kind_code, kind_code.replace("_", " ").title())},
    )

    session = (
        PerformanceSession.objects
        .filter(player=player, session_kind_ref=kind_obj, session_date=session_date)
        .order_by("id")
        .first()
    )
    created = False
    if session is None:
        session = PerformanceSession.objects.create(
            player=player,
            session_kind_ref=kind_obj,
            session_date=session_date,
            week=week,
            source_legacy_table=source_tag,
            source_legacy_id=0,
        )
        created = True
    else:
        if week is not None and session.week != week:
            session.week = week
            session.save(update_fields=["week", "updated_at"])

    for code, raw_value in metrics.items():
        value = _to_float_or_none(raw_value)
        if value is None:
            continue
        metric_type = PerformanceMetricType.objects.filter(code=code).first()
        if metric_type is None:
            continue
        PerformanceMetric.objects.update_or_create(
            session=session,
            metric_type=metric_type,
            defaults={"value": value},
        )
    return session, created


def mean(values: Iterable[float]) -> float:
    vals = [float(v) for v in values]
    return (sum(vals) / len(vals)) if vals else 0.0
