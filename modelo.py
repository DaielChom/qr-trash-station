from flask_sqlalchemy import SQLAlchemy

# Inicializa base de datos
db = SQLAlchemy()

class Estacion(db.Model):
    __tablename__ = "estacion"

    id_estacion = db.Column(db.String(1000), primary_key = True, nullable= False)
    descripcion = db.Column(db.String(1000), nullable= False)

    def __init__(self, id_estacion, descripcion):
        self.id_estacion = id_estacion
        self.descripcion = descripcion

class Reporte(db.Model):

    __tablename__ = "reporte"

    id_reporte = db.Column(db.String(1000), nullable=False, primary_key=True)
    estacion_reporte = db.Column(db.String(1000), db.ForeignKey('estacion.id_estacion'), nullable=False)
    estado_reporte = db.Column(db.String(1000), nullable=False)
    fecha_reporte = db.Column(db.String(1000), nullable=False)
    nombre_usuario_reporte = db.Column(db.String(1000), nullable=True)
    correo_usuario_report = db.Column(db.String(1000), nullable=True)
    url_imagen_reporte = db.Column(db.String(1000), nullable=False)
    ubicacion_reporte = db.Column(db.String(1000), nullable=False)

    def __init__(self, id_reporte, estacion_reporte, estado_reporte, fecha_reporte, nombre_usuario_reporte, correo_usuario_report, url_imagen_reporte, ubicacion_reporte):
        self.id_reporte = id_reporte
        self.estacion_reporte = estacion_reporte
        self.estado_reporte =estado_reporte
        self.fecha_reporte = fecha_reporte
        self.nombre_usuario_reporte = nombre_usuario_reporte
        self.correo_usuario_report = correo_usuario_report
        self.url_imagen_reporte = url_imagen_reporte
        self.ubicacion_reporte = ubicacion_reporte
