import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

from ..utils.parser import instantiate_dataclass

logger = logging.getLogger(__name__)


class ResumeExporter:
    def __init__(
        self,
        source_filepath: str,
        template_filepath: str,
    ) -> None:
        with open(source_filepath, "r") as f:
            data = yaml.safe_load(f)
        self.resume = instantiate_dataclass("Resume", data)
        path = Path(template_filepath)
        env = Environment(loader=FileSystemLoader(str(path.parent)))
        template = env.get_template(path.name)
        self.template = template.render(resume=self.resume)

    def to_http(self) -> None:
        def make_request_handler(html):
            class MyRequestHandler(SimpleHTTPRequestHandler):
                def do_GET(self):
                    if self.path == "/":
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(html.encode())
                    else:
                        super().do_GET()

            return MyRequestHandler

        handler_class = make_request_handler(self.template)
        httpd = HTTPServer(("localhost", 8000), handler_class)
        print("ready at http://localhost:8000/")
        httpd.serve_forever()
