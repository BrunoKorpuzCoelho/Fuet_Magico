import logging
from apps.core.models import ErrorLog


class DatabaseErrorHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.WARNING:
            try:
                ErrorLog.objects.create(
                    level=record.levelname,
                    message=record.getMessage(),
                    traceback=self.format(record) if record.exc_info else None,
                    request_path=getattr(record, 'request_path', None),
                    user=getattr(record, 'user', None)
                )
            except Exception:
                self.handleError(record)
