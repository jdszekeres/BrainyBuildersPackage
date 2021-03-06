from flask import *
import os
app = Flask(__name__)
@app.route("/favicon.ico")
@app.route("/apple-touch-icon-precomposed.png")
@app.route("/apple-touch-icon.png")
@app.route("/favicon.png")
@app.route("/favicon-coast.png")
@app.route("/apple-touch-icon-<size>-precomposed.png")

def favicon(size=""):
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
@app.route('/')
def index():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)