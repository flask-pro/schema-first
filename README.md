# Schema-First

Validate and convert OpenAPI specification via Marshmallow schemas to Marshmallow schemas.

<!--TOC-->

- [Schema-First](#schema-first)
  - [Features](#features)
  - [Installation](#installation)
  - [Example](#example)
  - [Additional documentation](#additional-documentation)

<!--TOC-->

## Features

* OpenAPI specification validate.
* Convert OpenAPI schemas to Marshmallow schemas.

## Installation

Recommended using the latest version of Python. Schema-First supports Python 3.14 and newer.

Install and update using `pip`:

```shell
$ pip install -U schema_first
```

## Example

Create specification - `openapi.yaml`:
```yaml
openapi: 3.1.1
info:
    title: Example API for testing Flask-First
    version: 1.0.1
paths:
    /endpoint:
        get:
            operationId: endpoint
            responses:
                '200':
                    content:
                        application/json:
                            schema:
                                properties:
                                    message:
                                        type: string
                                type: object
                    description: OK


```
Create script - `main.py`:
```python
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

```

More example see to `./example` folder.

## Additional documentation

* [OpenAPI Documentation](https://swagger.io/specification/).
* [OpenAPI on GitHub](https://github.com/OAI/OpenAPI-Specification).
* [JSON Schema Documentation](https://json-schema.org/specification.html).
