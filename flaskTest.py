__author__ = 'zheng'


from flask import Flask, request
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/post/<int:post_id>')
def post(post_id):
    #return 'user: ' + username + request.path
    #return request.args.get('q', '')
    return "postid: %s" % post_id

@app.route('/para', methods=['GET', 'POST'])
def para_extract():
    p1 = request.values.get('user', 'unknown')
    p2 = request.values.get('pass', 'secret')
    print request.args # get
    print request.form # post
    print request.values # combine
    return "%s : %s " % (p1, p2)
    #return '%s' % 0.5689

@app.route('/sim', methods=['GET', 'POST'])
def sim():
    p1 = request.values.get('word1', 'unknown')
    p2 = request.values.get('word2', 'unknown')
    return '%s' % 0.5689

if __name__ == "__main__":
    app.debug = True
    #app.run()
    app.run(host='0.0.0.0')