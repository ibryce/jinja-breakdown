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
STATIC_URL = '/static/'

# Base context for templates
base_context = {
    'STATIC_URL': STATIC_URL,
}

class BreakdownHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ Custom request handler """

    def not_found(self):
        """ Standard 404 response """
        self.send_error(httplib.NOT_FOUND, 'Document not found: %s' % self.path)
        return False

    def serve_static(self, path):
        """ Return data from path based on its guessed MIME Type """
        try:
            # Attempt to open path
            file = open(get_static(path))

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

        except (jinja2.TemplateNotFound, IOError):
            return self.not_found()

    def do_GET(self):
        """ Handle a GET request """
        if self.path.startswith(STATIC_URL):
            # Serve as static
            return self.serve_static(os.path.relpath(self.path, STATIC_URL))
        elif self.path.endswith('.html'):
            # Serve as template
            return self.serve_template(self.path)
        else:
            # Try appending /index.html, or .html
            try:
                path = self.path
                if not path.endswith('/'):
                    path = path + '/'
                env.get_template(path + 'index.html')
                self.serve_template(path + 'index.html')
            except jinja2.TemplateNotFound:
                path = self.path
                if path.endswith('/'):
                    path = path[:-1]
                self.serve_template(path + '.html')

def run_server():
    try:
        server = BaseHTTPServer.HTTPServer((ADDR, PORT), BreakdownHandler)
        print 'Server listening on port %s...' % PORT
        server.serve_forever()
    except socket.error:
        print 'Unable to bind socket (perhaps another server is running?)'


def get_static(path):
    """ Try to retrieve a static file by looking through static_dirs in order """
    for dir in static_dirs:
        fullpath = os.path.join(dir, path)
        if os.path.exists(fullpath):
            return fullpath
    raise IOError

def ver(self, opt, value, parser):
    print '.'.join(map(str, VERSION))
    sys.exit()

if __name__ == '__main__':
    # Populate options
    op = optparse.OptionParser(usage='%prog (PATH) [OPTIONS]')
    op.add_option('-o', '--old', action='store_true', dest='old', 
                  help='use single toplevel templates and static directories')
    op.add_option('-m', '--media', action='store_true', dest='media',
                  help='treat MEDIA_URL as STATIC_URL in templates')
    op.add_option('-v', '--version', action='callback', 
                  help='display the version number and exit', callback=ver)

    # Parse arguments
    (options, args) = op.parse_args()

    # Setup path globals
    if len(args) > 0:
        root = args[0]
    else:
        root = os.getcwd()
    root = os.path.abspath(root)

    if options.media:
        # Update context
        base_context['MEDIA_URL'] = STATIC_URL

    if options.old:
        # Don't use apps, use single templates and static directories
        template_dirs = [os.path.join(root, 'templates')]
        if not os.path.exists(template_dirs[0]):
            print 'No template directory found at', template_dirs[0]
            sys.exit(1)
        static_dirs = [os.path.join(root, 'static')]
        if not os.path.exists(static_dirs[0]):
            print 'No static directory found at', static_dirs[0]
            sys.exit(1)
    else:
        # Build apps list
        app_dirs = []
        if not os.path.exists(os.path.join(root, 'apps')):
            print('No apps directory found!  Make sure to run breakdown from the '
            'project root, or specify a project root as an argument.  If your '
            'templates are in toplevel, try the `--old` option')
            sys.exit(2)
        else:
            appspath = os.path.join(root, 'apps')
            files = [os.path.join(appspath, file) for file in os.listdir(appspath) if not
                     file.startswith('.')]
            app_dirs = filter(os.path.isdir, files)

        # Setup template and static dirs
        template_dirs = [os.path.join(dir, 'templates') for dir in app_dirs]
        static_dirs = [os.path.join(dir, 'static') for dir in app_dirs]

    # Setup jinja2 global
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dirs))

    # Run program
    run_server()