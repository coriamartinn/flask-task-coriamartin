# IMPORTACIONES
from flask import Flask
from flask_mysqldb import MySQL
from config import Config
from models.tareas_db import TareasDB
from routes.tareas import crear_blueprint_tareas

# CREACION INSTANCIA DE LA APP DE FLASK
app = Flask(__name__)
app.config.from_object(Config)

# CONEXION DE LA BASE DE DATOS
mysql = MySQL(app)
tareas_db = TareasDB(mysql)

# REGISTRO DE LOS BLUESPRINTS (LAS RUTAS)
tareas_bp = crear_blueprint_tareas(tareas_db)
app.register_blueprint(tareas_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5847)
