import http.cookiejar, urllib.request, os, stat, json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

os.chmod("./service_worker.js", stat.S_IRWXU)
os.chmod("./index.html", stat.S_IRWXU)


class RequestHandler(BaseHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods',
                     'GET, POST, PUT, DELETE, OPTIONS')
    self.send_header('Access-Control-Allow-Headers',
                     'Origin, X-Requested-With, Content-Type, Accept')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.end_headers()
    os.system("clear")

  def do_OPTIONS(self):
    self.send_response(200, "ok")
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods',
                     'GET, POST, PUT, DELETE, OPTIONS')
    self.send_header("Access-Control-Allow-Headers",
                     "Origin, X-Requested-With, Content-Type, Accept")
    self.send_header("Access-Control-Allow-Headers", "Content-Type")
    self.end_headers()

  def _send_response(self, content, content_type='text/html'):
    self.send_response(200)
    self.send_header('Content-type', content_type)
    self.end_headers()
    self.wfile.write(bytes(content, "utf8"))
    os.system("clear")

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    parsed_data = json.loads(post_data.decode())
    try:
      # Create a cookie jar
      cj = http.cookiejar.CookieJar()

      # Create an opener to handle the cookies
      opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj))

      # Add a user-agent to the headers
      headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
      }

      # Create a Request object
      req = urllib.request.Request(parsed_data["url"], headers=headers)

      # Make a request to the webpage
      response = opener.open(req)

      os.system('clear')

      # Read the response
      html = response.read().decode('utf-8', errors='ignore')
      self._send_response(self.handle_images(html, parsed_data["url"]))
    except Exception as e:
      # If the request is not successful, handle the error
      self._send_response(str(e))
      self.send_error(500)

  def do_GET(self):
    try:
      with open("index.html", "r") as file:
        html = file.read()
        self._send_response(html)
    except:
      self.send_error(404)
      self.end_headers()

  def handle_images(self, html, url):
    """
            Handle image tags by replacing the src attribute with the full url.
            """

    os.system('clear')

    base_url = urlparse(url).scheme + "://" + urlparse(url).hostname
    new_html = html.replace("src=\"/", f"src=\"{base_url}/")
    return new_html


def run(server_class=HTTPServer, handler_class=RequestHandler, port=443):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print(f'Starting httpd on port {port}...')
  httpd.serve_forever()


run()
