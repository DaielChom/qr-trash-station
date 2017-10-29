# Libraries
from flask import Flask
from flask import render_template
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from flask import request
import json
import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import zbarlight

from modelo import db
from modelo import Estacion
from modelo import Reporte

# Init Flask
app = Flask(__name__)

# Implement config
app.config.from_object(DevelopmentConfig)

# Implement Security for forms
csrf = CSRFProtect()

# Rute /
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/stations' , methods=['POST'])
def stations():

    estacion_q = Estacion(request.form['id'])
    db.session.add(estacion_q)
    db.session.commit()
    ##devoler QR
    return json.dumps({'OK':200})

@app.route('/report' , methods=['GET'])
def report():
    return render_template('report.html')

@app.route('/admin' , methods=['GET', 'POST'])
def admin():
    informes = Reporte.query.all() ##ARREGLAR QUERY
    return render_template('admin.html', informes = informes)

@app.route('/qrdecode', methods=['POST'])
def qrdecode():
    s = request.form['image'][22:]
    img_b = base64.b64decode(s)
    buf = io.BytesIO(img_b)
    buf = mpimg.imread(buf, format='JPG')
    codes = zbarlight.scan_codes('qrcode', Image.fromarray(buf))
    if codes is not None:
        qr_id = str(codes[0])[2:]
    else:
        qr_id = None
    return json.dumps({'id':qr_id})

if __name__ == '__main__':

    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run()
