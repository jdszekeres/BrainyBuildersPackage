from flask import *
app = Flask(__name__)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('/static', "favicon.ico")
@app.route('/')
def index():
    return render_template("index.html")
app.run(debug=False, port=8000)