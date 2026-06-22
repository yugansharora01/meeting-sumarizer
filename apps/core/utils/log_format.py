"""Formatters used by settings.LOGGING for the `app` logger.

JsonLineFormatter  -> one JSON object per line, written to logs/app.jsonl
ConsoleFormatter   -> short, human-readable line for the terminal
"""

import json
import logging
from datetime import datetime, timezone


def _record_payload(record):
    """Build the dict we serialize for a log record."""
    base = {
        "ts": datetime.fromtimestamp(record.created, tz=timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "level": record.levelname.lower(),
        "logger": record.name,
    }

    data = getattr(record, "event_data", None)
    if isinstance(data, dict):
        base.update(data)
    else:
        # Fall back gracefully for plain logger.info("text") calls.
        base["message"] = record.getMessage()

    if record.exc_info:
        base["exc_info"] = logging.Formatter().formatException(record.exc_info)

    return base


class JsonLineFormatter(logging.Formatter):
    def format(self, record):
        # default=str so things like datetime / UUID / Decimal never crash a log.
        return json.dumps(_record_payload(record), default=str, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    """Compact one-liner: `HH:MM:SS LEVEL [group/event] key=value ...`"""

    _RESERVED = {"ts", "level", "logger", "group", "event"}

    def format(self, record):
        p = _record_payload(record)
        ts = p["ts"][11:19]  # HH:MM:SS
        group = p.get("group", record.name)
        event = p.get("event", "")
        head = f"{group}/{event}" if event else group

        extras = []
        for k, v in p.items():
            if k in self._RESERVED or k == "message" or k == "exc_info":
                continue
            sv = v if isinstance(v, str) else json.dumps(v, default=str, ensure_ascii=False)
            if len(sv) > 200:
                sv = sv[:197] + "..."
            extras.append(f"{k}={sv}")

        line = f"{ts} {p['level'].upper():<7} [{head}]"
        if "message" in p:
            line += f" {p['message']}"
        if extras:
            line += " " + " ".join(extras)
        if p.get("exc_info"):
            line += "\n" + p["exc_info"]
        return line
