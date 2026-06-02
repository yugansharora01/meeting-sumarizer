from apps.core.exceptions import AppException
from rest_framework.views import exception_handler
from apps.core.utils import response
import logging

logger = logging.getLogger(__name__)

def custom_handler(exc,context):
    res = exception_handler(exc,context)
    if res is not None:
        data = res.data
        detail = "An error occurred"
        if isinstance(data, dict):
            detail = data.get("detail", str(data))
        elif data is not None:
            detail = str(data)

        return response.error(
            detail,
            res.status_code,
        )
    
    if isinstance(exc,AppException):
        return response.error(exc.message,exc.status_code)
    
    logger.exception("Unhandled Exception",exc_info=exc)

    return response.error("Internal Server Error",500)
