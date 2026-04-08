#!/usr/bin/env python3
"""
Effective Mobile – Backend HTTP Server
Listens on port 8080, accessible only within Docker network.
"""

import json
import logging
import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("APP_PORT", 8080))
HOST = os.environ.get("APP_HOST", "0.0.0.0")


class AppHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002
        logger.info("%s - %s", self.address_string(), format % args)

    def _send(self, code: int, content_type: str, body: str):
        encoded = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("X-Powered-By", "Effective Mobile Backend")
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/":
            self._send(200, "text/plain; charset=utf-8", "Hello from Effective Mobile!")

        elif self.path == "/health":
            payload = json.dumps({"status": "ok", "service": "backend"})
            self._send(200, "application/json", payload)

        elif self.path == "/api/ping":
            payload = json.dumps({
                "message": "Hello from Effective Mobile!",
                "status": "ok",
                "service": "backend",
            })
            self._send(200, "application/json", payload)

        else:
            self._send(404, "text/plain; charset=utf-8", "Not Found")


def shutdown(signum, frame):
    logger.info("Received signal %s, shutting down…", signum)
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    server = HTTPServer((HOST, PORT), AppHandler)
    logger.info("Backend listening on %s:%s", HOST, PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        logger.info("Server stopped.")