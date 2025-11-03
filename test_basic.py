"""
Minimal test to verify Python runs on Azure
"""
print("Python is working!")
print("Starting basic HTTP server...")

from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello from Azure! Python is working.')

    def log_message(self, format, *args):
        print(f"Request: {format % args}")

if __name__ == "__main__":
    port = int(os.environ.get("WEBSITES_PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"Server started on port {port}")
    server.serve_forever()
