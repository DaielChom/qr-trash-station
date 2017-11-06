# Libraries
from flask import Flask, redirect, url_for
from flask import render_template
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
    return redirect(url_for('report'))

@app.route('/stations' , methods=['POST'])
def stations():
    stations_id = request.form['id']
    estacion_q = Estacion(stations_id)
    db.session.add(estacion_q)
    db.session.commit()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(Config.SERVER_NAME+"/rpt/"+stations_id)
    qr.make(fit=True)
    qr = qr.make_image()

    qr.save("./static/img/qr/"+stations_id+".jpeg", "jpeg")
    return json.dumps({'qr':"/static/img/qr/"+stations_id+".jpeg"})

@app.route('/rpt' , methods=['GET','POST'])
@app.route('/rpt/<id_estacion>' , methods=['GET'])
def report(id_estacion = None):

    if request.method == 'GET' and id_estacion is None:
        return render_template('report.html')

    if request.method == 'GET' and id_estacion:

        ## ID id_estacion exist in the db

        return render_template('form.html', id_estacion=id_estacion)

    if request.method == 'POST':
        img = getImageToB64(request.form['img'])
        mpimg.imsave("./static/img/rpt/"+"REPORT_"+request.form['id']+"_"+request.form['fecha_report']+".jpg",img, format="jpg", dpi=150)
        informe = Reporte("REPORT"+request.form['id']+request.form['ubicacion'], request.form['id'], request.form['estado'], request.form['fecha_report'], request.form['nombre'], "./static/img/rpt/"+"REPORT_"+request.form['id']+"_"+request.form['fecha_report']+".jpg" ,request.form['ubicacion'])
        db.session.add(informe)
        db.session.commit()
        return json.dumps({'ok':200})

@app.route('/admin' , methods=['GET', 'POST'])
def admin():
    informes = Reporte.query.all() ##ARREGLAR QUERY
    return render_template('admin.html', informes = informes)

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
