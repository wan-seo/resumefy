import sys

from src.lib import ResumeExporter

if __name__ == "__main__":
    source_path = sys.argv[1]
    template_path = sys.argv[2]
    exporter = ResumeExporter(source_path, template_path)
    exporter.to_http()
