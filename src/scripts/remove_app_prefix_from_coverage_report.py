import xml.etree.ElementTree as ET
from pathlib import Path


def remove_app_prefix_from_coverage_report():
    coverage_path = Path(__file__).parent.parent / "coverage.xml"
    tree = ET.parse(coverage_path)
    root = tree.getroot()
    for sources_elem in root.iter("sources"):
        for source_elem in sources_elem.iter("source"):
            if source_elem.text.startswith("/app/"):
                source_elem.text = source_elem.text.replace("/app/", "", 1)

    tree.write(coverage_path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    remove_app_prefix_from_coverage_report()
