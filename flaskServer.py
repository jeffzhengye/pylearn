import flaskTest, flaskTest.views
import os

app = flaskTest.Flask(__name__)


app.secrect_key = 'python_key'

class View(flaskTest.views.MethodView):
	def get(self):
		return "hello world"
		

	def post(self):
		a = flaskTest.request.form('query')
		return "post works"


class Remote(flaskTest.views.MethodView):
	def get(self):
		return flaskTest.render_template('index.html')


	def post(self):
		result = eval(flaskTest.request.form['expression'])
		flaskTest.flash(result)
		return self.get()


app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])
app.add_url_rule('/', view_func=Remote.as_view('remote'), methods=['GET', 'POST'])

app.debug = True

app.run()