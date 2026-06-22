"""
Structured JSON logger for the project.

Instead of scattering ``print()`` everywhere, call one of the helpers below.
Every call writes one JSON object per line to ``logs/app.jsonl`` (and a short,
readable line to the console). Pass any keyword arguments you want recorded --
they are stored as JSON, so API/webhook payloads stay queryable.

Examples
--------
    from apps.core.utils.logger import applog

    # Result of an outgoing API call
    applog.api("recall.create_bot", request=payload, response=data, status=201)

    # Incoming webhook
    applog.webhook("recall", event=event, data=data, bot_id=bot_id)

    # Anything else, with your own group + arbitrary fields to filter on later
    applog.log("meetings", "created", meeting_id=m.id, user=str(user))

    # Errors (level=error, accepts exc_info)
    applog.error("recall", "create_bot failed", exc=str(e), status=500)

The ``group`` (and every keyword you pass) can be used to filter/group when
viewing logs:  ``python manage.py logs --group webhook --where event=bot.done``
"""

import logging

# Plain logger name; the JSON file + console handlers are wired up in
# settings.LOGGING under this name.
_logger = logging.getLogger("app")


def _emit(group, event=None, level="info", exc_info=False, **fields):
    payload = {"group": group}
    if event is not None:
        payload["event"] = event
    # Everything else the caller passed becomes a top-level JSON field so it can
    # be filtered on with `manage.py logs --where key=value`.
    payload.update(fields)

    log_fn = getattr(_logger, level, _logger.info)
    # The actual JSON serialization happens in the formatter (settings.LOGGING),
    # which reads `event_data` off the record.
    log_fn("%s", payload.get("event") or group, extra={"event_data": payload},
           exc_info=exc_info)


class _AppLog:
    """Thin namespace so call sites read as ``applog.api(...)`` etc."""

    def log(self, group, event=None, level="info", **fields):
        """Generic structured log. `group` is your grouping key."""
        _emit(group, event=event, level=level, **fields)

    def api(self, name, *, status=None, level="info", **fields):
        """Result of an (outgoing) API call. `name` e.g. 'recall.create_bot'."""
        if status is not None:
            fields["status"] = status
        _emit("api", event=name, level=level, **fields)

    def webhook(self, provider, *, event=None, level="info", **fields):
        """An incoming webhook. `provider` e.g. 'recall'."""
        _emit("webhook", event=event or provider, level=level,
              provider=provider, **fields)

    def info(self, group, event=None, **fields):
        _emit(group, event=event, level="info", **fields)

    def warning(self, group, event=None, **fields):
        _emit(group, event=event, level="warning", **fields)

    def error(self, group, event=None, *, exc_info=False, **fields):
        _emit(group, event=event, level="error", exc_info=exc_info, **fields)


applog = _AppLog()
