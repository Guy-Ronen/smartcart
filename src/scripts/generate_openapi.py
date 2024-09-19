from pathlib import Path

import yaml

from smart_cart.main import app


def generate_openapi_schema_file():
    src_path = Path(__file__).parent.parent
    with open(f"{src_path}/openapi.yml", "w") as file:
        yaml.dump(app.openapi(), file)
    print("OpenAPI schema file created!")


if __name__ == "__main__":
    generate_openapi_schema_file()
