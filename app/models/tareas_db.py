from flask_mysqldb import MySQL


class TareasDB:
    def __init__(self, mysql):
        self.mysql = mysql

    def obtener_todas(self):
        """Obtiene todas las tareas de la base de datos"""
        with self.mysql.connection.cursor() as cur:
            cur.execute('SELECT * FROM tareas')
            tareas = cur.fetchall()  # Trae todas las filas
            cur.close()
            return [{"id": t[0], "titulo": t[1], "descripcion": t[2], "estado": t[3]} for t in tareas]
    def obtener_por_id(self, id):
        """Obtiene una tarea específica por su ID"""
        with self.mysql.connection.cursor() as cur:
            cur.execute('SELECT * FROM tareas WHERE id = %s', (id,))
            return cur.fetchone()  # Trae solo una fila

    def agregar(self, titulo, descripcion, estado):
        """Agrega una nueva tarea a la base de datos y devuelve su ID"""
        with self.mysql.connection.cursor() as cur:
            cur.execute(
                'INSERT INTO tareas (titulo, descripcion, estado) VALUES (%s, %s, %s)',
                (titulo, descripcion, estado)
            )
            self.mysql.connection.commit()
            return cur.lastrowid  # Devuelve el ID insertado

    def actualizar(self, id, titulo, descripcion, estado):
        """Actualiza una tarea existente en la base de datos"""
        with self.mysql.connection.cursor() as cur:
            cur.execute("""
                UPDATE tareas
                SET titulo = %s, descripcion = %s, estado = %s
                WHERE id = %s
            """, (titulo, descripcion, estado, id))
            self.mysql.connection.commit()

    def eliminar(self, id):
        """Elimina una tarea de la base de datos por su ID"""
        with self.mysql.connection.cursor() as cur:
            cur.execute('DELETE FROM tareas WHERE id = %s', (id,))
            self.mysql.connection.commit()
