# Libraries
import time
from flask import Flask, redirect, url_for
from flask import render_template, session
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from config import Config
from flask import request
import json
import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
from modelo import db
from modelo import Estacion
from modelo import Reporte

# Init Flask
app = Flask(__name__)

# Implement config
app.config.from_object(DevelopmentConfig)

# Implement Security for forms
csrf = CSRFProtect()

def getImageToB64(code):
    s = code[22:]
    img_b = base64.b64decode(s)
    buf = io.BytesIO(img_b)
    buf = mpimg.imread(buf, format='JPG')
    return buf

# Rute /
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if 'acceso' in session:
        session.pop('acceso')

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':

        user = request.form['user']
        passw = request.form['pass']

        if (user=="admin" and passw == "1234"):
            session['acceso'] = "true"
            return json.dumps({'acceso':'true'})

        else:
            return json.dumps({'acceso':'false'})


@app.route('/stations' , methods=['POST'])
def stations():
    stations_id = request.form['id']
    descripcion = request.form['descripcion']
    estacion_q = Estacion(stations_id, descripcion)
    db.session.add(estacion_q)
    db.session.commit()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data("http://"+Config.SERVER_NAME+"/rpt/"+stations_id)
    qr.make(fit=True)
    qr = qr.make_image()

    qr.save("./static/img/qr/"+stations_id+".jpeg", "jpeg")
    return json.dumps({'qr':"/static/img/qr/"+stations_id+".jpeg"})

@app.route('/rpt' , methods=['POST'])
@app.route('/rpt/<id_estacion>' , methods=['GET'])
def report(id_estacion = None):

    #if request.method == 'GET' and id_estacion is None:
    #    return render_template('report.html')

    if request.method == 'GET' and id_estacion:

        ## ID id_estacion exist in the db

        return render_template('form.html', id_estacion=id_estacion)

    if request.method == 'POST':

        dir_image = "none"

        if request.form['img'] != "0":
            img = getImageToB64(request.form['img'])
            dir_image = "./static/img/rpt/"+"REPORT_"+request.form['id']+"_"+ time.strftime("%d-%m-%Y:%H:%M:%S")+".jpg"
            mpimg.imsave(dir_image,img, format="jpg", dpi=150)

        informe = Reporte("REPORT"+request.form['id']+request.form['ubicacion']+time.strftime("%d/%m/%Y:%H:%M:%S"), request.form['id'], request.form['estado'], time.strftime("%d-%m-%Y"), request.form['nombre'],request.form['correo'], dir_image ,request.form['ubicacion'])
        db.session.add(informe)
        db.session.commit()
        return json.dumps({'ok':200})

@app.route('/gestion' , methods=['GET', 'POST'])
def admin():
    if 'acceso' in session:
        informes = Reporte.query.all() ##ARREGLAR QUERY
        estaciones = Estacion.query.all()
        return render_template('admin.html', informes = informes, estaciones = estaciones)
    else:
        return "Acceso denegado"


@app.route('/qrdecode', methods=['POST'])
def qrdecode():
    buf = getImageToB64(request.form['image'])
    codes = decode(Image.fromarray(buf))

    if codes is not None:
        qr_id = str(codes[0].data)[2:-1]
    else:
        qr_id = None
    return json.dumps({'id':qr_id})

if __name__ == '__main__':

    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(host = '0.0.0.0')
