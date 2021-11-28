from flask import *
import os
import db
import qrcode
import base64
from io import BytesIO
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="inportant buisness {-;")
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
    agent = request.user_agent.string
    print(agent)
    mobile = "iphone" in agent.lower() or "android" in agent.lower() or " Opera Mini" in agent or "BB10" in agent
    if request.args.get("override") != None:
            return render_template("not found.html")
    info = db.select_package(package)
    if info == None:
        return render_template("not found.html", notfound=True, mobile=mobile)
    print(info)
    return render_template("package.html", info=info, locations=info[2], mobile=mobile)
@app.route("/create/package", methods=["POST", "GET"])
def create_package():
    if request.method == "POST":
        if request.form.get('check'):
            db.__package_say_goodlbye(request.form.get("override"), [], request.form.get('adress'))
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
            print(request.form.get('override'))
            pack = request.host_url+"/package/"+str(request.form.get('override'))
            print(pack)
            qr.add_data(pack)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            return render_template("confetti.html", hi=img_str.decode('utf-8'))
        if request.form.get('id') == 'package':
            v = db.add_package([], request.form.get('adress'))
        else:
            v = db.add_package([], request.form.get('adress'), id=request.form.get('id'))

        print(request.form.get('id'))
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(request.host_url+"/package/"+str(v))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return  render_template("confetti.html", hi=img_str.decode('utf-8'))
    else:
        return render_template("not found.html", notfound=False)
@app.route("/update/<package>", methods=["POST"])
def update_package(package):
    try:
        v = geolocator.reverse(request.form.get('newlocation')).address
    except:
        v = request.form['newlocation']
    db.update_packages(package, location = v)
    return redirect(request.referrer)
@app.route('/test')
def test():
    abort(500)
@app.errorhandler(500)
def error500(e):
    return """<p><span style="color: #800000;">roses are red</span></p>
    <p><span style="color: #00ffff;">violets are blue</span></p>
    <p>{} in line 10,042</p>""".format(e)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)