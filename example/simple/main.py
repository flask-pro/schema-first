from pathlib import Path
from pprint import pprint

from schema_first.specification import Specification

spec_file = Path('openapi.yaml')
spec = Specification(spec_file)
spec.load()

pprint(spec.reassembly_spec)
print(
    'Marshmallow schema generated from OpenAPI schema',
    spec.reassembly_spec['paths']['/endpoint']['get']['responses']['200']['content'][
        'application/json'
    ]['schema'],
)
