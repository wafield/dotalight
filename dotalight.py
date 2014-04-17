import os
import sys
import cgi
import jinja2

PYPATH = os.path.dirname(os.path.realpath(__file__))
if PYPATH not in sys.path:
    sys.path.append(PYPATH)

import database
import html

def application(environ, start_response):
    # Reload html page everytime. This is good for debugging.
    reload(html)
    
    method = environ['REQUEST_METHOD'].upper()
    if method == 'POST':
        # the environment variable CONTENT_LENGTH may be empty or missing
        request_body_size = int(environ.get('CONTENT_LENGTH', '0'))

        # When the method is POST the query string will be sent
        # in the HTTP request body which is passed by the WSGI server
        # and sent via the wsgi.input environment variable.
        request_body = environ['wsgi.input'].read(request_body_size)
        # post_data is a dictory storing data from client
        post_data = cgi.parse_qs(request_body)
    elif method == 'GET':
        get_data = cgi.parse_qs(environ['QUERY_STRING'])
    else:
        # This branch should be unreachable 
        pass
    
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

