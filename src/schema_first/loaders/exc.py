from ..exceptions import SchemaFirstException


class YAMLReaderError(SchemaFirstException):
    """Exception for yaml file loading error."""


class ResolverError(SchemaFirstException):
    """Exception for specification from yaml file resolver error."""
