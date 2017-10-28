# Libraries
from flask import Flask
from flask import render_template
from flask_wtf import CSRFProtect
from config import DevelopmentConfig

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
    return "stations"

@app.route('/report' , methods=['GET'])
def report():
    return "report"

@app.route('/admin' , methods=['GET', 'POST'])
def admin():
    return "admin"

@app.route('/reports' , methods=['GET'])
def reports():
    return "reports"

if __name__ == '__main__':
    csrf.init_app(app)
    app.run()
