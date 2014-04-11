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
    status = '200 OK'
    output = html.HTML['portal']

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

