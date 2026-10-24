"""MCP server for Cron Schedule Expression Parser and Next Run Evaluator."""
import sys
import json
from datetime import datetime
from client import CronScheduleEvaluator


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "get_next_cron_runs",
                    "description": "Calculates the next upcoming execution timestamps for a standard 5-field cron expression",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "cron_expression": {"type": "string", "description": "Standard 5-field crontab string (e.g. '*/15 * * * *')"},
                            "count": {"type": "integer", "default": 5},
                            "start_iso": {"type": "string", "description": "Optional ISO start datetime"},
                        },
                        "required": ["cron_expression"],
                    },
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "get_next_cron_runs":
            start_dt = None
            if args.get("start_iso"):
                start_dt = datetime.fromisoformat(args["start_iso"])
            runs = CronScheduleEvaluator.get_next_runs(
                cron_expr=args.get("cron_expression", "* * * * *"),
                start_datetime=start_dt,
                count=int(args.get("count", 5)),
            )
            return {"content": [{"type": "text", "text": json.dumps({"next_runs": runs}, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
