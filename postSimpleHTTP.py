import urllib2
import urllib
import time
import httplib, mimetypes
 
HOST = '127.0.0.1'
PORT = '8080' 
 
def post_multipart(host, port, selector, fields, files):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        content_type, body = encode_multipart_formdata(fields, files)
        h = httplib.HTTP(host, port)
        h.putrequest('POST', '/cgi-bin/query')
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        #errcode, errmsg, headers = h.getreply()
        h.getreply()
        return h.file.read() 
 
def encode_multipart_formdata(fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        if fields:
                for (key, value) in fields:
                        L.append('--' + BOUNDARY)
                        L.append('Content-Disposition: form-data; name="%s"' % key)
                        L.append('')
                        L.append(value)
        if files:
                for (key, filename, value) in files:
                        # L.append('--' + BOUNDARY)
                        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
                        L.append('Content-Type: %s' % get_content_type(filename))
                        L.append('')
                        L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body =  CRLF.join(L)
        print "body: \n", body, "\n End body"
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body 
 
def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream' 

def post():
    import httplib, urllib
    params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost:8080")
    conn.request("POST", "/cgi-bin/query", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()


def test():
        print  post_multipart(HOST, PORT, 'markuz',
                                        ( ('username','markuz'),  ('another_field','another value')),
                                        (('query','query','Query'), ),
                                   ) 
 
if __name__ == '__main__':      
     test()