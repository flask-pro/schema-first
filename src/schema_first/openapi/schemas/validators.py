from marshmallow.exceptions import ValidationError
from marshmallow.validate import Validator


class VersionMatch(Validator):
    """Version specification validator check minor and major parts from string.
     The patch part is not meaningful.

    :param comparable: The object to compare to.
    :param error: Error message to raise in case of a validation error.
        Can be interpolated with `{input}` and `{other}`.
    """

    default_message = 'Version {input} must be start with {other}.'

    def __init__(self, comparable, *, error: str | None = None):
        self.comparable = comparable
        self.error: str = error or self.default_message

    def _repr_args(self) -> str:
        return f"comparable={self.comparable!r}"

    def _format_error(self, value: str) -> str:
        return self.error.format(input=value, other=self.comparable)

    def __call__(self, value: str) -> str:
        if not value.startswith(f'{self.comparable}.'):
            raise ValidationError(self._format_error(value))
        return value
