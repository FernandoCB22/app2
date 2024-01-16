# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
import io
from openpyxl import Workbook


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/aplicacion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Bootstrap(app)


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    documentacion = db.Column(db.String(9), unique=True, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.Enum('M', 'F'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(25), nullable=False)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['Nombre']
        apellidos = request.form['Apellidos']
        documentacion = request.form['Documentacion']
        edad = request.form['Edad']
        genero = request.form['Genero']
        email = request.form['Correo']
        telefono = request.form['Telefono']

        # Crear un nuevo usuario y agregarlo a la base de datos
        nuevo_usuario = Usuario(nombre=nombre, apellidos=apellidos, documentacion=documentacion, edad=edad, genero=genero, email=email, telefono=telefono)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)


@app.route('/resultados', methods=['GET'])
def resultados():
    # Obtén los parámetros de búsqueda del formulario
    nombre = request.args.get('nombre', '')
    apellidos = request.args.get('apellidos', '')
    documento = request.args.get('documento', '')
    edad = request.args.get('edad', '')
    genero = request.args.get('genero', '')
    correo = request.args.get('correo', '')
    telefono = request.args.get('telefono', '')

    # Construye la consulta SQL basada en los parámetros de búsqueda
    consulta = Usuario.query

    if nombre:
        consulta = consulta.filter(Usuario.nombre.ilike(f"%{nombre}%"))
    if apellidos:
        consulta = consulta.filter(Usuario.apellidos.ilike(f"%{apellidos}%"))
    if documento:
        consulta = consulta.filter(Usuario.documentacion.ilike(f"%{documento}%"))
    if edad:
        consulta = consulta.filter(Usuario.edad.ilike(f"%{edad}%"))
    if correo:
        consulta = consulta.filter(Usuario.email.ilike(f"%{correo}%"))
    if telefono:
        consulta = consulta.filter(Usuario.telefono.ilike(f"%{telefono}%"))
    
    # Solo incluir el filtro por género si se proporciona en el formulario
    if genero and genero in ('M', 'F'):
        consulta = consulta.filter(Usuario.genero == genero)
    else:
            # Si no se proporciona género, no aplicar filtro por género
        consulta = consulta.filter()

    # Obtén los resultados de la consulta
    resultados = consulta.all()

    # Renderiza la plantilla 'resultados.html' con los resultados
    return render_template('resultados.html', resultados=resultados)


@app.route('/altausuario')
def alta_usuario():
    return render_template('altausuario.html')

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        documentacion = request.form['documento']
        edad = request.form['edad']
        genero = request.form['genero']
        email = request.form['correo']
        telefono = request.form['telefono']

        # Crear un nuevo usuario y agregarlo a la base de datos
        nuevo_usuario = Usuario(nombre=nombre, apellidos=apellidos, documentacion=documentacion, edad=edad,
                                genero=genero, email=email, telefono=telefono)
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Redirigir a la página de búsqueda (o a donde desees después de registrar)
        return redirect(url_for('.index'))

# Definir la función para obtener los resultados de la búsqueda
def obtener_resultados(nombre, apellidos, documento, edad, genero, correo, telefono):
    # Construir la consulta SQL basada en los parámetros de búsqueda
    consulta = Usuario.query

    if nombre:
        consulta = consulta.filter(Usuario.nombre.ilike(f"%{nombre}%"))
    if apellidos:
        consulta = consulta.filter(Usuario.apellidos.ilike(f"%{apellidos}%"))
    if documento:
        consulta = consulta.filter(Usuario.documentacion.ilike(f"%{documento}%"))
    if edad:
        consulta = consulta.filter(Usuario.edad.ilike(f"%{edad}%"))
    if genero:
        consulta = consulta.filter(Usuario.genero.ilike(f"%{genero}%"))
    if correo:
        consulta = consulta.filter(Usuario.email.ilike(f"%{correo}%"))
    if telefono:
        consulta = consulta.filter(Usuario.telefono.ilike(f"%{telefono}%"))

    resultados = consulta.all()

    return resultados


if __name__ == '__main__':
    app.run(debug=True)