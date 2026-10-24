"""Cron Schedule Expression Parser and Next Run Evaluator.
100% Python Standard Library.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Set, Any, Optional


class CronScheduleEvaluator:
    """Parses standard 5-field UNIX crontab expressions (* * * * *) and computes
    upcoming deterministic execution timestamps."""

    FIELD_RANGES = [
        ("minute", 0, 59),
        ("hour", 0, 23),
        ("day_of_month", 1, 31),
        ("month", 1, 12),
        ("day_of_week", 0, 6),  # 0 = Sunday, 6 = Saturday
    ]

    @classmethod
    def _parse_field(cls, field_str: str, min_val: int, max_val: int) -> Set[int]:
        """Parses a single cron field with support for *, */step, range (1-5), and lists (1,3,5)."""
        values = set()
        sub_parts = field_str.split(",")

        for part in sub_parts:
            part = part.strip()
            if not part:
                continue

            if part == "*":
                values.update(range(min_val, max_val + 1))
            elif "/" in part:
                range_part, step_part = part.split("/", 1)
                step = int(step_part)
                start = min_val if range_part in ("*", "") else int(range_part)
                values.update(range(start, max_val + 1, step))
            elif "-" in part:
                start_str, end_str = part.split("-", 1)
                values.update(range(int(start_str), int(end_str) + 1))
            else:
                values.add(int(part))

        # Filter strictly within valid boundaries
        return {v for v in values if min_val <= v <= max_val}

    @classmethod
    def parse_expression(cls, cron_expr: str) -> Dict[str, Set[int]]:
        """Parses a 5-field cron expression into allowed sets of values."""
        fields = cron_expr.strip().split()
        if len(fields) != 5:
            raise ValueError(f"Invalid cron expression '{cron_expr}': expected 5 fields, got {len(fields)}.")

        parsed = {}
        for (name, min_v, max_v), raw_f in zip(cls.FIELD_RANGES, fields):
            parsed[name] = cls._parse_field(raw_f, min_v, max_v)
        return parsed

    @classmethod
    def get_next_runs(
        cls,
        cron_expr: str,
        start_datetime: Optional[datetime] = None,
        count: int = 5,
        max_search_days: int = 366,
    ) -> List[str]:
        """Computes the next 'count' scheduled execution datetimes starting after start_datetime."""
        parsed = cls.parse_expression(cron_expr)
        curr = (start_datetime or datetime.now()).replace(second=0, microsecond=0) + timedelta(minutes=1)

        results = []
        limit_date = curr + timedelta(days=max_search_days)

        while len(results) < count and curr < limit_date:
            # Check month
            if curr.month not in parsed["month"]:
                # Jump to next month
                if curr.month == 12:
                    curr = datetime(curr.year + 1, 1, 1, 0, 0)
                else:
                    curr = datetime(curr.year, curr.month + 1, 1, 0, 0)
                continue

            # Check day of month and day of week
            # Python weekday: Monday is 0, Sunday is 6 -> convert to cron 0=Sun..6=Sat
            cron_weekday = (curr.weekday() + 1) % 7
            day_matches = (curr.day in parsed["day_of_month"]) and (cron_weekday in parsed["day_of_week"])
            if not day_matches:
                curr = (curr + timedelta(days=1)).replace(hour=0, minute=0)
                continue

            # Check hour
            if curr.hour not in parsed["hour"]:
                curr = (curr + timedelta(hours=1)).replace(minute=0)
                continue

            # Check minute
            if curr.minute not in parsed["minute"]:
                curr = curr + timedelta(minutes=1)
                continue

            # All match!
            results.append(curr.isoformat())
            curr = curr + timedelta(minutes=1)

        return results
