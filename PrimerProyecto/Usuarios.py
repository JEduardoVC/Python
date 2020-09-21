from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import mysql.connector

app = Flask(__name__)

class Connection:
     def run_query(self, nombres = None, apellidos = None, fechaNacimiento = None, generos = None, id = None):
          conexion1=mysql.connector.connect(host="localhost", user="root", passwd="", database="primerproyectopython")
          cursor1=conexion1.cursor()
          if nombres is not None and apellidos is not None and fechaNacimiento is not None and generos is not None and id is None:
               cursor1.execute("INSERT INTO usuarios_python(nombre, apellidos, fecha_nacimiento, genero) values (%s, %s, %s, %s)", (nombres, apellidos, fechaNacimiento, generos))
               conexion1.commit()

          if nombres is None and apellidos is None and fechaNacimiento is None and generos is None and id is None:
               cursor1.execute("SELECT * FROM primerproyectopython.usuarios_python")
               lista = cursor1.fetchall()
               conexion1.close()
               cursor1.close()
               return lista

          if nombres is None and apellidos is None and fechaNacimiento is None and generos is None and id is not None:
                    cursor1.execute("DELETE FROM primerproyectopython.usuarios_python WHERE id_usuario = {}".format(id))
                    conexion1.commit()
          
          conexion1.close()
          cursor1.close()

@app.route('/')
def index():
     now = datetime.now()
     c = Connection()
     lista = c.run_query()
     return render_template('usuarios.html', nombre="José Eduardo Valencia Camacho", fecha = now, lista = lista)

@app.route('/usuario',methods=['POST'])
def about():
     conexion = Connection()
     nombres = request.form['nombre']
     apellidos = request.form['apellido']
     fechaNacimiento = request.form['fechaNacimiento']
     generos = request.form['genero']
     conexion.run_query(nombres, apellidos, fechaNacimiento, generos, None)
     return redirect(url_for("index"))

@app.route('/borrarUsuario/<string:id>')
def borrarUsuario(id):
     con = Connection()
     con.run_query(None, None, None, None, id)
     return redirect(url_for("index"))

if __name__ == '__main__':
     app.run()