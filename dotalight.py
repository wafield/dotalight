import os
import sys
import cgi
import jinja2
import json
import time

PYPATH = os.path.dirname(os.path.realpath(__file__))
if PYPATH not in sys.path:
    sys.path.append(PYPATH)

import html
import service

def application(environ, start_response):
    # Reload html page everytime. This is good for debugging.
    reload(html)

    method = environ['REQUEST_METHOD'].upper()
    post_data = {}
    get_data = {}

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
        if post_data.get('update', ['0'])[0] == '1' and post_data.get('vanity_url', []):
            content_type = 'text/plaintext'
            vanity_url = post_data['vanity_url'][0]
            ret = service.update_player_profile(vanity_url)
            if ret[0]:
                output = 'SUCCESS<br><a href="/dotalight/%d">GO TO PLAYER PROFILE</a>' % (ret[1])
            else:
                output = 'FAILED'
        else:
            content_type = 'text/html'
            output = html.HTML['portal']
    elif url_path.find('/') == -1 and url_path.isdigit():
        steamid = int(url_path)
        if post_data.get('ajax', ['0'])[0] == '1':
            content_type = 'text/plaintext'
            heroid = int(post_data.get('heroid', ['0'])[0])
            output = service.render_dashboard(steamid, heroid, True)
        else:
            content_type = 'text/html'
            output = service.render_dashboard(steamid)
    elif url_path.find('/') != -1:
        items = url_path.split('/')
        if len(items) == 2:
            steamid = url_path.split('/')[0]
            trendid = url_path.split('/')[1]
            output = service.trend(int(steamid), trendid)
            content_type = 'text/html'
            output = output.encode('ascii', 'ignore')
    else:
        output = 'Unkown Request!'
        content_type = 'text/plaintext'

    response_headers = [('Content-Type', content_type),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
