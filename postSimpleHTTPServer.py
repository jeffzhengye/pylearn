# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import cgi
import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
 
class customHTTPServer(BaseHTTPRequestHandler):
        def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('<HTML><body>Get!</body></HTML>')
                return 
                
        def do_POST(self):
        # Parse the form data posted
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                             'CONTENT_TYPE':self.headers['Content-Type'],
                             })

                # Begin the response
                self.send_response(200)
                self.end_headers()
                self.wfile.write('Client: %s\n' % str(self.client_address))
                self.wfile.write('Path: %s\n' % self.path)
                self.wfile.write('Form data:\n')

                # Echo back information about what was posted in the form
                print "form: ", form
                for field in form.keys():
                    print field, " type: ", type(field)
                    # field_item = form[field].upper()
                    print form.getvalue(field), type(form.getvalue(field))
                    field_item = form.getvalue(field).upper()
                    print field_item
                    # if field_item.filename:
                    #     # The field contains an uploaded file
                    #     file_data = field_item.file.read()
                    #     file_len = len(file_data)
                    #     del file_data
                    #     self.wfile.write('\tUploaded %s (%d bytes)\n' % (field, 
                    #                   
                    #     print '\tUploaded %s (%d bytes)\n' % (field, 
                    #                                                      file_len)
                    # else:
                    #     # Regular form value
                    #     self.wfile.write('\t%s=%s\n' % (field, form[field].value))
                    #     print '\t%s=%s\n' % (field, form[field].value)
                return
        
                
def main():
        try:
                server = HTTPServer(('',8080),customHTTPServer)
                print 'server started at port 8080'
                server.serve_forever()
        except KeyboardInterrupt:
                server.socket.close() 
 
if __name__=='__main__':
        main()