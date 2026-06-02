class AppException(Exception):
    status_code=400
    default_message="Something went wrong"

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)

class ValidationError(AppException):
    status_code=400
    default_message="Validation failed"

class ExternalServiceError(AppException):
    status_code=502
    default_message="External Service error"