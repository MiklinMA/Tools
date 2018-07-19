#!/usr/bin/env python
#
# 2018
# Mike Miklin <MiklinMA@gmail.com>
#
# Simple redirect from HTTP to HTTPs
# without Apache or Nginx
#


from __future__ import print_function
try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer
except ImportError:
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer

class RedirectHandler(SimpleHTTPRequestHandler):
   def do_GET(self):
       url = 'https://%s%s' % (
           self.headers.get('Host'),
           self.path
       )
       self.send_response(301)
       self.send_header('Location', url)
       self.end_headers()

def main():
    try:
        handler = TCPServer(('0.0.0.0', 80), RedirectHandler)
    except Exception as e:
        print("error:", str(e))
        return
    try:
        print('Server started')
        handler.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

