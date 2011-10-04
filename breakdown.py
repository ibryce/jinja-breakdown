#!/usr/bin/env python
""" 
    Breakdown.py - 2011 Concentric Sky

    Lightweight jinja2 template prototyping server with support for
    some custom template tags
"""
VERSION = (0, 2, 0)

import os
import sys
import optparse
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
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()

            # Render the template and write to stream
            data = template.render(base_context)
            self.wfile.write(data.encode('utf-8'))
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
            path = self.path
            if path.endswith('/'):
                path = path[:-1]
            return self.serve_template(path + '.html')

def main():
    # Validate paths
    if not os.path.exists(template_path):
        print 'Warning: unable to find template directory', template_path
    else:
        print 'Serving templates from', template_path
    if not os.path.exists(static_path):
        print 'Warning: unable to find static data directory', static_path
    else:
        print 'Serving static data from', static_path

    # Run server
    try:
        server = BaseHTTPServer.HTTPServer((ADDR, PORT), BreakdownHandler)
        print 'Server listening on port %s...' % PORT
        server.serve_forever()
    except socket.error:
        print 'Unable to bind socket (perhaps another server is running?)'


def ver(self, opt, value, parser):
    print '.'.join(map(str, VERSION))
    sys.exit()

if __name__ == '__main__':
    # Populate options
    op = optparse.OptionParser(usage='%prog (PATH) [OPTIONS]')
    op.add_option('-v', '--version', action='callback', 
                  help='display the version number and exit', callback=ver)

    # Parse arguments
    (options, args) = op.parse_args()

    # Setup path globals
    if len(args) > 1:
        root = args[0]
    else:
        root = os.getcwd()
    
    root = os.path.abspath(root)
    static_path = os.path.join(root, 'static')
    template_path = os.path.join(root, 'templates')

    # Setup jinja2 global
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))

    # Run program
    main()