# genpark-cron-schedule-expression-parser-and-next-run-evaluator-skill

Standard 5-field cron expression parser, interval evaluator, and upcoming execution schedule generator.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Standard 5-Field Crontab Support**: Parses `minute hour day-of-month month day-of-week` specifications.
- **Complex Step, Range & List Syntax**: Handles wildcard steps (`*/15`), hyphenated ranges (`1-5`, `9-17`), and comma-separated lists (`1,15,30`).
- **Calendar-Aware Leap & Month Rollout**: Accurately computes future run timestamps across varying month lengths and weekend boundaries.
- **Pure Native Python DateTime Evaluation**: Runs in microsecond latency with zero third-party scheduling binaries.

## Architecture

```
[Cron Expression: "* / 15 9-17 * * 1-5" + Start DateTime]
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                CronScheduleEvaluator                   │
│  - 5-Field Range & Step Boundary Parser                │
│  - Calendar Month Day & Weekday Synchronizer           │
│  - Next-N Sequential Occurrence Calculator             │
│  - ISO-8601 Timestamp Formatter                        │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
[Chronological Upcoming Execution Timestamp List]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `get_next_cron_runs`: Calculates the next upcoming execution timestamps for a standard 5-field cron expression.

## Quickstart (Python API)

```python
from client import CronScheduleEvaluator

runs = CronScheduleEvaluator.get_next_runs("0 9 * * 1-5", count=3)
print("Next 9 AM Weekday Runs:", runs)
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
