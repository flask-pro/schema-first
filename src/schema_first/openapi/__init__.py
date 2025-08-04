from pathlib import Path
from pprint import pformat

from marshmallow import ValidationError

from ..loaders.yaml_loader import load_from_yaml
from .exc import OpenAPIValidationError
from .schemas.v3_1_1.root_schema import RootSchema


class OpenAPI:
    def __init__(self, path: Path or str):
        self.path = path
        self.raw_spec = load_from_yaml(self.path)

    def load(self) -> dict:
        try:
            return RootSchema().load(self.raw_spec)
        except ValidationError as e:
            raise OpenAPIValidationError(f'\n{pformat(e.messages)}')
