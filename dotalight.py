import os
import sys

PYPATH = os.path.dirname(os.path.realpath(__file__))
if PYPATH not in sys.path:
    sys.path.append(PYPATH)

import cgi
import jinja2
import database
import html

def application(environ, start_response):
    reload(html)

    status = '200 OK'

    url_path = environ['PATH_INFO'][1:]  # The trailing part of the requested URL

    if url_path == '':
        content_type = 'text/html'
        output = html.HTML['portal']
    elif url_path.find('/') == -1 and url_path.startswith('account_'):
        vanity_url = url_path[8:]
        output = '<html><head><title>Test Page</title></head><body><p>Requested User Profile: %s</p></body></html>' % (vanity_url)
        content_type = 'text/html'
    else:
        output = 'Unkown Request!'
        content_type = 'text/plaintext'

    response_headers = [('Content-Type', content_type),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

