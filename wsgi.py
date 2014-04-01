# Note: configure httpd
# https://help.ubuntu.com/10.04/serverguide/httpd.html
# a2ensite depweb

# Consider using a more modern server such as python twisted

# Note: need to put deppkg from dependency-graph-process project onto PYTHONPATH
# Note: setup symbolic link from static/code to chrome23/src/
#     /dependency-depweb/static$ ln -s /home/dchollak/projects/chrome23/src/ code

HOST_NAME = 'localhost'
HOST_PORT = 8051

import sys, os
from wsgiref.simple_server import make_server

PYPATH = os.path.dirname(os.path.realpath(__file__))
print >> sys.stderr, PYPATH
if PYPATH not in sys.path:
    sys.path.append(PYPATH)

import dotalight

def wsgi(environ, start_response):
    return dotalight.application(environ, start_response)

httpd = make_server(HOST_NAME, HOST_PORT, wsgi)
print >> sys.stderr, "Starting server on: " + str(HOST_NAME) + ":" + str(HOST_PORT)
httpd.serve_forever()
