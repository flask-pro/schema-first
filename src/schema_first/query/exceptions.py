"""The module contains the exceptions used in the Flask-First extension."""


class QueryValidatorException(Exception):
    """Common exception."""


class EndpointValidation(QueryValidatorException):
    """Exception for endpoint validation error."""


class MethodValidation(QueryValidatorException):
    """Exception for method validation error."""


class ContentTypeValidation(QueryValidatorException):
    """Exception for content type validation error."""


class StatusCodeValidation(QueryValidatorException):
    """Exception for status code validation error."""


class MethodParametersValidation(QueryValidatorException):
    """Exception for parameters validation error."""


class RequestHeadersValidation(QueryValidatorException):
    """Exception for headers validation error."""


class RequestCookiesValidation(QueryValidatorException):
    """Exception for cookies validation error."""


class PathParametersValidation(QueryValidatorException):
    """Exception for path-parameters validation error."""


class QueryParametersValidation(QueryValidatorException):
    """Exception for request arguments validation error."""


class RequestCookieValidation(QueryValidatorException):
    """Exception for request cookie validation error."""


class RequestJSONValidation(QueryValidatorException):
    """Exception for JSON validation error."""


class ResponseJSONValidation(QueryValidatorException):
    """Exception for response validation error."""
