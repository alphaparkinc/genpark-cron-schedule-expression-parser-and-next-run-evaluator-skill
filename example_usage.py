"""Example usage for Cron Schedule Expression Parser and Next Run Evaluator."""
from datetime import datetime
from client import CronScheduleEvaluator


def main():
    base_time = datetime(2026, 10, 24, 12, 0, 0)
    print(f"Base Time: {base_time.isoformat()}")

    print("\n=== 1. Every 15 Minutes ('*/15 * * * *') ===")
    runs_15m = CronScheduleEvaluator.get_next_runs("*/15 * * * *", start_datetime=base_time, count=4)
    for r in runs_15m:
        print("  ->", r)

    print("\n=== 2. Weekdays at 9:30 AM ('30 9 * * 1-5') ===")
    runs_weekday = CronScheduleEvaluator.get_next_runs("30 9 * * 1-5", start_datetime=base_time, count=3)
    for r in runs_weekday:
        print("  ->", r)

    print("\n=== 3. First of Every Month at Midnight ('0 0 1 * *') ===")
    runs_monthly = CronScheduleEvaluator.get_next_runs("0 0 1 * *", start_datetime=base_time, count=3)
    for r in runs_monthly:
        print("  ->", r)


if __name__ == "__main__":
    main()
