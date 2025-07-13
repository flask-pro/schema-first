from pathlib import Path

import yaml
from marshmallow import ValidationError

from .exc import OpenAPIValidationError
from .schemas.v3_1_1.root_schema import RootSchema


class OpenAPI:
    def __init__(self, path: Path or str):
        self.path = path
        self.raw_spec = self._yaml_to_dict(self.path)

    @staticmethod
    def _yaml_to_dict(path: Path) -> dict:
        with open(path) as f:
            s = yaml.safe_load(f)
        return s

    def load(self) -> None or OpenAPIValidationError:
        try:
            return RootSchema().load(self.raw_spec)
        except ValidationError as e:
            raise OpenAPIValidationError(e)
