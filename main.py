# Libraries
from flask import Flask
from flask import render_template
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from flask import request
import json

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
    ## ADD TO BD
    print(request.form)
    return json.dumps({'OK':200})

@app.route('/report' , methods=['GET'])
def report():
    return "report"

@app.route('/admin' , methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route('/reports' , methods=['GET'])
def reports():
    return "reports"

if __name__ == '__main__':
    csrf.init_app(app)
    app.run()
