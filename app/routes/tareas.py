from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask.views import MethodView
from flask_mysqldb import MySQL
from models.tareas_db import TareasDB
import MySQLdb.cursors

def crear_blueprint_tareas(tareas_db):
    tareas_bp = Blueprint('tareas', __name__)

    # clase para listar/mostrar en el index las tareas

    class VistaTareas(MethodView):
        def get(self):
            tareas = tareas_db.obtener_todas()
            return render_template('index.html', tareas=tareas)

    # CLASE agregar tareas a la db

    class AgregarTareas(MethodView):
        def get(self):
            return render_template('agregar_tarea.html')

        def post(self):
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            estado = request.form['estado']
            cur = tareas_db.mysql.connection.cursor()
            tareas_db.agregar(titulo, descripcion, estado)
            flash('Se agregó correctamente la tarea', "success")
            return redirect(url_for('tareas.vista_tareas'))

    # clase eliminar tarea

    class EliminarTareas(MethodView):
        def get(self, id):
            tareas_db.eliminar(id)
            flash('La tarea ha sido eliminada correctamente.', "success")
            return redirect(url_for('tareas.vista_tareas'))

    # clase editar tarea

    class EditarTarea(MethodView):
        def get(self, id):
            cur = tareas_db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM tareas WHERE id = %s", (id,))
            tarea = cur.fetchone()  # <-- Posible problema
            cur.close()
            return render_template('editar_tarea.html', tarea=tarea)

    class ActualizarTarea(MethodView):
        def post(self, id):
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            estado = request.form['estado']
            tareas_db.actualizar(id, titulo, descripcion, estado)
            flash('Se actualizo correctamente', 'success')
            return redirect(url_for('tareas.vista_tareas'))

    tareas_bp.add_url_rule('/', view_func=VistaTareas.as_view('vista_tareas'))
    tareas_bp.add_url_rule('/agregar_tarea',
                           view_func=AgregarTareas.as_view('agregar_tarea'), methods=['GET', 'POST'])
    tareas_bp.add_url_rule('/editar_tarea/<int:id>',
                           view_func=EditarTarea.as_view('editar_tarea'))
    tareas_bp.add_url_rule('/actualizar_tarea/<int:id>',
                           view_func=ActualizarTarea.as_view('actualizar_tarea'), methods=['POST'])
    tareas_bp.add_url_rule('/eliminar_tarea/<int:id>',
                           view_func=EliminarTareas.as_view('eliminar_tarea'))

    return tareas_bp
