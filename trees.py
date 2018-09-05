import json
from http.server import HTTPServer, BaseHTTPRequestHandler

'''
*******************************

Create a simple web server, using only the standard library packages of your
choice of python, go or nodejs, that does the following:

    Only accepts POST requests.

    For any request, checks the body for a json encoded object and returns a
    descriptive HTTP error code if the body does not contain a valid json
    object.
    We expect this object to look like this:  {"favoriteTree": "baobab"}

    Only accepts requests on the index URL: "/", and returns the proper HTTP
    error code if a different URL is requested.

    Runs locally on port 8000.

    For a successful request, returns a properly encoded HTML document with the
    following content:

        If "favoriteTree" was specified:
            It's nice to know that your favorite tree is a
            <value of "favoriteTree" in the POST body>!

        If not specified:
            Please tell me your favorite tree.

*******************************
'''


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def method_not_allowed(self):
        self.send_response(405)
        self.end_headers()
        self.wfile.write(bytes('405 Method not allowed', 'UTF-8'))

    def do_GET(self):
        self.method_not_allowed()

    def do_PUT(self):
        self.method_not_allowed()

    def do_PATCH(self):
        self.method_not_allowed()

    def do_DELETE(self):
        self.method_not_allowed()

    def do_POST(self):
        status = 200
        content_type = 'text/plain'
        response = ''

        if self.path != '/':
            status = 404
            response = '404 Not Found'

        request_content_type = self.headers['Content-Type']
        if not request_content_type or \
                request_content_type != 'application/json':
            status = 415
            response = '415 Unsupported Media Type'

        content_len = int(self.headers['content-length'])
        payload = self.rfile.read(content_len).decode()

        if status == 200:
            try:
                json_payload = json.loads(payload)

                try:
                    favoriteTree = json_payload['favoriteTree']
                except KeyError:
                    print("That's a crooked tree. We'll send him to \
                          Washington.")
                    favoriteTree = None

                if favoriteTree and favoriteTree != '':
                    print('Talk to the tree, make friends with it.')
                    response = "It's nice to know that your favorite tree " + \
                        'is a ' + favoriteTree + '!'
                else:
                    response = 'Please tell me your favorite tree.'
            except json.decoder.JSONDecodeError as error:
                print("We don't make mistakes. We just have happy accidents.")
                print(error)

                status = 422
                response = '422 Unprocessable Entity'

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

        self.wfile.write(bytes(response, 'UTF-8'))


def run():
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Running server on 127.0.0.1:8000...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Closing the server.')
        httpd.server_close()

run()
