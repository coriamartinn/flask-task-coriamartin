# IMPORTACIONES
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL

# CREACION INSTANCIA DE LA APP DE FLASK
app = Flask(__name__)

# CONFIGURACION DE LA BASE DE DATOS (db)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud_tareas'

# CONEXION DE LA BASE DE DATOS
mysql = MySQL(app)


@app.route('/', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tareas')
    tareas = cur.fetchall()

    return render_template('index.html', tareas=tareas)


@app.route('/agregar_tarea', methods=['GET', 'POST'])
def agregar_tarea():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tareas (titulo, descripcion, estado) VALUES (%s, %s, %s)',
                    (titulo, descripcion, estado))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return render_template('agregar_tarea.html')


@app.route('/editar_tarea/<id>', methods=['GET', 'POST'])
def editar_tarea(id):

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tareas WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('editar_tarea.html', tareas=data[0])

# UPDATEAR TAREAS


@app.route('/updates/<id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE tareas
                    SET titulo = %s,
                        descripcion = %s,
                        estado = %s
                    WHERE id = %s
                    """, (titulo, descripcion, estado, id))
        mysql.connection.commit()
        flash('Se actualizo correctamente', 'success')
        return redirect(url_for('index'))


# SECRET KEY
app.secret_key = 'msg-flash'

# VISTA PARA ELIMINAR LAS TAREAS DE LA BASE DE DATOS


@app.route('/delete/<string:id>')
def eliminar_tarea(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tareas WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('La tarea ha sido eliminada correctamente.', "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5847)
