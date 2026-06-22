"""
View structured app logs without grepping JSON by hand.

The `applog` helper (apps/core/utils/logger.py) writes one JSON object per line
to logs/app.jsonl. This command reads that file and lets you filter, group and
pretty-print those entries.

Examples
--------
    # last 50 entries (default)
    python manage.py logs

    # only webhooks, last 100
    python manage.py logs --group webhook -n 100

    # filter by any field stored in the entry (repeatable)
    python manage.py logs --where event=bot.done --where provider=recall

    # group entries by a field and show a count + the entries under each
    python manage.py logs --group-by event

    # just the counts per group
    python manage.py logs --group-by group --count

    # show the full pretty JSON of each entry (great for API/webhook payloads)
    python manage.py logs --group api --full

    # live tail (like `tail -f`)
    python manage.py logs --follow
"""

import json
import time
from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "View / filter / group the structured app logs (logs/app.jsonl)."

    def add_arguments(self, parser):
        parser.add_argument("--group", help="Filter by group (e.g. api, webhook).")
        parser.add_argument("--event", help="Filter by event name.")
        parser.add_argument("--level", help="Filter by level (info, warning, error...).")
        parser.add_argument(
            "--where",
            action="append",
            default=[],
            metavar="KEY=VALUE",
            help="Filter by any field. Repeatable. e.g. --where bot_id=abc",
        )
        parser.add_argument(
            "--group-by",
            dest="group_by",
            metavar="FIELD",
            help="Group entries by a field (e.g. event, group, status).",
        )
        parser.add_argument(
            "--count",
            action="store_true",
            help="With --group-by, only show counts per group.",
        )
        parser.add_argument(
            "-n",
            "--tail",
            type=int,
            default=50,
            help="Show only the last N matching entries (0 = all). Default 50.",
        )
        parser.add_argument(
            "--full",
            action="store_true",
            help="Pretty-print the full JSON of each entry.",
        )
        parser.add_argument(
            "--follow",
            "-f",
            action="store_true",
            help="Keep the file open and print new entries as they arrive.",
        )
        parser.add_argument(
            "--file",
            help="Path to a log file (default: settings.APP_LOG_FILE).",
        )

    # -- helpers ---------------------------------------------------------

    def _log_path(self, opts):
        return opts.get("file") or str(
            getattr(settings, "APP_LOG_FILE", settings.BASE_DIR / "logs" / "app.jsonl")
        )

    def _parse_where(self, where):
        filters = {}
        for item in where:
            if "=" not in item:
                raise ValueError(f"--where expects KEY=VALUE, got: {item!r}")
            key, value = item.split("=", 1)
            filters[key.strip()] = value.strip()
        return filters

    def _matches(self, entry, opts, where):
        if opts.get("group") and str(entry.get("group")) != opts["group"]:
            return False
        if opts.get("event") and str(entry.get("event")) != opts["event"]:
            return False
        if opts.get("level") and str(entry.get("level")) != opts["level"]:
            return False
        for key, value in where.items():
            if str(entry.get(key)) != value:
                return False
        return True

    def _read_entries(self, path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            return

    # -- rendering -------------------------------------------------------

    def _render(self, entry, full):
        if full:
            return json.dumps(entry, indent=2, ensure_ascii=False, default=str)
        ts = str(entry.get("ts", ""))[11:19]
        level = str(entry.get("level", "")).upper()
        group = entry.get("group", "")
        event = entry.get("event", "")
        head = f"{group}/{event}" if event else group
        reserved = {"ts", "level", "logger", "group", "event"}
        extras = []
        for key, value in entry.items():
            if key in reserved:
                continue
            sv = value if isinstance(value, str) else json.dumps(
                value, ensure_ascii=False, default=str
            )
            if len(sv) > 200:
                sv = sv[:197] + "..."
            extras.append(f"{key}={sv}")
        line = f"{ts} {level:<7} [{head}]"
        if extras:
            line += " " + " ".join(extras)
        return line

    # -- main ------------------------------------------------------------

    def handle(self, *args, **opts):
        path = self._log_path(opts)
        try:
            where = self._parse_where(opts["where"])
        except ValueError as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
            return

        if opts["follow"]:
            self._follow(path, opts, where)
            return

        entries = [e for e in self._read_entries(path) if self._matches(e, opts, where)]

        if opts["tail"] and opts["tail"] > 0:
            entries = entries[-opts["tail"]:]

        if not entries:
            self.stdout.write(self.style.WARNING(f"No matching log entries in {path}"))
            return

        if opts["group_by"]:
            self._render_grouped(entries, opts)
        else:
            for entry in entries:
                self.stdout.write(self._render(entry, opts["full"]))

    def _render_grouped(self, entries, opts):
        field = opts["group_by"]
        buckets = defaultdict(list)
        for entry in entries:
            buckets[str(entry.get(field))].append(entry)

        for key in sorted(buckets):
            bucket = buckets[key]
            header = f"=== {field}={key}  ({len(bucket)}) ==="
            self.stdout.write(self.style.HTTP_INFO(header))
            if not opts["count"]:
                for entry in bucket:
                    self.stdout.write("  " + self._render(entry, opts["full"]).replace("\n", "\n  "))
                self.stdout.write("")

    def _follow(self, path, opts, where):
        self.stdout.write(self.style.NOTICE(f"Following {path} (Ctrl-C to stop)..."))
        # Print existing tail first.
        existing = [e for e in self._read_entries(path) if self._matches(e, opts, where)]
        if opts["tail"] and opts["tail"] > 0:
            existing = existing[-opts["tail"]:]
        for entry in existing:
            self.stdout.write(self._render(entry, opts["full"]))

        try:
            with open(path, "r", encoding="utf-8") as fh:
                fh.seek(0, 2)  # jump to end
                while True:
                    line = fh.readline()
                    if not line:
                        time.sleep(0.4)
                        continue
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if self._matches(entry, opts, where):
                        self.stdout.write(self._render(entry, opts["full"]))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Log file not found: {path}"))
        except KeyboardInterrupt:
            self.stdout.write("\nStopped.")
