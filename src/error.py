class APIError(Exception):
    """All custom API Exceptions"""
    pass


class APIBadRequestError(APIError):
    """Bad Request Error Class."""
    code = 400
    description = "Bad request Error"


class APIInternalServerError(APIError):
    """Internal Server Error Class."""
    code = 500
    description = "Internal Server Error"

