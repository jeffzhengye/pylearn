__author__ = 'zheng'

import re

script = re.compile(r'<script.*?</script>', re.M | re.DOTALL)


def remove_adsense():
    import urllib
    url = "http://google-dictionary.so8848.com/meaning?word=maps"
    f = urllib.urlopen(url)
    content = f.read()
    matches = script.finditer(content)
    remove_list = []
    for m in matches:
        print m.span()
        code = m.group(0)
        if code.find('google_ad_slot') != -1:
            print code
            remove_list.append(m.span())
        print '--'*100
    begin = 0
    content_new = []
    for start, end in remove_list:
        content_new.append(content[begin:start])
        begin = end
    content_new.append(content[end:])
    print ''.join(content_new)

remove_adsense()

#ct = """
#"""
#adsense.match(ct, re.M | re.DOTALL)
#
#ms = re.match(r'.*(<script.*?google_ad_client.*?</script>).*', ct, re.M|re.DOTALL)