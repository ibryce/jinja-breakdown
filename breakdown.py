#!/usr/bin/env python
""" 
    Breakdown.py - 2011 Concentric Sky

    Lightweight jinja2 template prototyping server with support for
    some custom template tags
"""

import os
import sys
import jinja2
import httplib
import mimetypes
import socket
import BaseHTTPServer

# Server settings
ADDR = ''
PORT = 5000
MEDIA_URL = '/static/'

# Paths to try (in order) for root request
index_defs = ['index.html']

# Base context for templates
base_context = {
    'MEDIA_URL': MEDIA_URL
}

class BreakdownHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ Custom request handler """

    def not_found(self):
        """ Standard 404 response """
        self.send_error(httplib.NOT_FOUND, 'Document not found: %s' % self.path)

    def serve_static(self, path):
        """ Return data from path based on its guessed MIME Type """
        try:
            # Attempt to open path
            file = open(os.path.join(static_path, path))

            # Send a successful header with guessed mimetype
            self.send_response(httplib.OK)
            self.send_header('Content-Type', mimetypes.guess_type(path)[0])
            self.end_headers()

            # Write data
            self.wfile.write(file.read())
            return

        except IOError:
            return self.not_found()
    
    def serve_template(self, path):
        """ Render a template file using jinja2 """
        try:
            # Attempt to open template
            template = env.get_template(path)

            # Send a success HTML header
            self.send_response(httplib.OK)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            # Render the template and write to stream
            data = template.render(base_context)
            self.wfile.write(data)
            return

        except jinja2.TemplateNotFound:
            return self.not_found()

    def do_GET(self):
        """ Handle a GET request """
        if self.path.startswith(MEDIA_URL):
            # Serve as static
            return self.serve_static(os.path.relpath(self.path, MEDIA_URL))
        elif self.path == '/':
            # Try index defaults
            for file in index_defs:
                if os.path.exists(os.path.join(template_path, file)):
                    return self.serve_template(file)
            return self.send_error(httplib.NOT_FOUND, 'Couldn\'t find an index document: ' 
                                   + ', '.join(index_defs))
        elif self.path.endswith('.html'):
            # Server as template
            return self.serve_template(self.path)
        else:
            # Finally try appending .html to the template
            return self.serve_template(self.path + '.html')

if __name__ == '__main__':
    # Setup paths
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = os.getcwd()
    
    root = os.path.abspath(root)
    static_path = os.path.join(root, 'static')
    template_path = os.path.join(root, 'templates')

    # Validate paths
    if not os.path.exists(template_path):
        print 'Warning: unable to find template directory', template_path
    else:
        print 'Serving templates from', template_path
    if not os.path.exists(static_path):
        print 'Warning: unable to find static data directory', static_path
    else:
        print 'Serving static data from', static_path

    # Setup jinja2
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))

    try:
        server = BaseHTTPServer.HTTPServer((ADDR, PORT), BreakdownHandler)
        print 'Server listening on port %s...' % PORT
        server.serve_forever()
    except socket.error:
        print 'Unable to bind socket (perhaps another server is running?)'
