import http.server
import socketserver
import os

class FileSaveHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        filename = self.path.lstrip('/')
        if not filename:
            self.send_response(400)
            self.end_headers()
            return
            
        print(f"Receiving {filename}...")
        os.makedirs("exported_models", exist_ok=True)
        filepath = os.path.join("exported_models", filename)
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        with open(filepath, 'wb') as f:
            f.write(post_data)
            
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Saved")

with socketserver.TCPServer(("", 8766), FileSaveHandler) as httpd:
    print("Serving on port 8766")
    httpd.serve_forever()
