import smtplib
import string
 
SUBJECT = "Test email from Python"
TO = "yezh0716@gmail.com"
FROM = "jeff.zheng.ye@gmail.com"
text = "blah blah blah"
BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        text
        ), "\r\n")
server = smtplib.SMTP('localhost')
server.sendmail(FROM, [TO], BODY)
server.quit()
print 'it is done '
