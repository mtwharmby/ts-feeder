from http.server import BaseHTTPRequestHandler, HTTPServer


class POSTHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_error(404, message="GET not available")

    def do_POST(self):
        if self.headers["Content-Type"] != "application/json":
            print(f"Wrong content type: {self.headers['Content-Type']}")
            self.send_error(
                400, message="Wrong content type",
                explain="POST on this server only accepts 'application/json'"
            )
        content_length = int(self.headers['Content-Length'])

        content = self.rfile.read(content_length)
        print(f"Headers: {self.headers}\nData: {content.decode('utf-8')}")

        self.send_response(200, message="OK")
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write("OK".encode("utf-8"))


with HTTPServer(("", 8000), POSTHandler) as server:
    server.serve_forever()

