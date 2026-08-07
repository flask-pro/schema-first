"""The module contains the exceptions used in the Flask-First extension."""


class QueryValidatorException(Exception):
    """Common exception."""


class EndpointValidation(QueryValidatorException):
    """Exception for endpoint validation error."""


class MethodValidation(QueryValidatorException):
    """Exception for method validation error."""


class RequestValidation(QueryValidatorException):
    """Exception for request validation error."""


class ResponseValidation(QueryValidatorException):
    """Exception for response validation error."""
