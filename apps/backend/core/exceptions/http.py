"""
HTTP exceptions
"""


class HttpException(Exception):
    """Base HTTP exception"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(HttpException):
    """404 Not Found"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class BadRequestException(HttpException):
    """400 Bad Request"""

    def __init__(self, message: str = "Bad request"):
        super().__init__(message, 400)


class UnauthorizedException(HttpException):
    """401 Unauthorized"""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)


class ConflictException(HttpException):
    """409 Conflict"""

    def __init__(self, message: str = "Conflict"):
        super().__init__(message, 409)
