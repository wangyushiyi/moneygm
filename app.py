from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ... [rest of your existing code] ...

# Add this at the end of the file
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

def handler(event, context):
    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = BytesIO()
            body.write(app.dispatch_request())
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body.getvalue())

    httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
    return httpd.handle_request()

# Keep this for local development
if __name__ == '__main__':
    app.run(debug=True)