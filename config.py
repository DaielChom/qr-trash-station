#Librerias a usar
import os

#   Las configuraciones se agrupan por funcionamineto
#   y se agrupan en clases.
#   'Cada clase es un set de configuraciones'

#Clase princial --Configuraciones en comun--
class Config(object):

    #Genera identificador para el formulario
    SECRET_KEY = 'SECRET_KEY'
    SERVER_NAME = '10.1.90.20:5000'
    APPLICATION_ROOT = 'contenedores'


#Clase Desarrollador --Configuraciones para el modo desarrollador--
class DevelopmentConfig(Config):

    #El servidor esta a la escucha de cambios
    DEBUG = True

    #Conexion con la base de datos Para MS SQL Server
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://user:pass@server/bd_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
