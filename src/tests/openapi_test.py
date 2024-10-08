from pathlib import Path

import yaml

from smart_cart.main import app


def test_openapi_spec():
    src_path = Path(__file__).parent.parent
    with open(f"{src_path}/openapi.yml") as file:
        stored_spec = yaml.safe_load(file)

    current_spec = app.openapi()

    assert stored_spec == current_spec
