#Librerias a usar
import os

#   Las configuraciones se agrupan por funcionamineto
#   y se agrupan en clases.
#   'Cada clase es un set de configuraciones'

#Clase princial --Configuraciones en comun--
class Config(object):

    #Genera identificador para el formulario
    SECRET_KEY = 'SECRET_KEY'
    SERVER_NAME = 'localhost:5000'

#Clase Desarrollador --Configuraciones para el modo desarrollador--
class DevelopmentConfig(Config):

    #El servidor esta a la escucha de cambios
    DEBUG = True

    #Conexion con la base de datos
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/qrtrash'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
