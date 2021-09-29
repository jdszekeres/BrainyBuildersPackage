from flask import *
import os
import db

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
@app.route("/package/<package>")
def package(package):
    if request.args.get("override") != None:
            return render_template("not found.html")
    info = db.select_package(package)
    if info == None:
        return render_template("not found.html")
    print(info)
    return render_template("package.html", info=info, locations=info[2])
@app.route("/create/package", methods=["POST"])
def create_package():
    if request.method == "POST":
        v = db.add_package([], request.form.get('adress'), id=request.form.get('id'))
        print(request.form.get('id'))
        return str(v)
    else:
        return "WIP"
@app.route("/update/<package>", methods=["POST"])
def update_package(package):
    db.update_packages(package, request.form.get('newlocation'))
    return redirect(request.referrer)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)