# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import tempfile
import os
import io
from openpyxl import Workbook


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/aplicacion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Bootstrap(app)


lista_temporal = []

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

@app.route('/generar_excel', methods=['GET'])
def generar_excel():
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
    if genero:
        consulta = consulta.filter(Usuario.genero.ilike(f"%{genero}%"))
    if correo:
        consulta = consulta.filter(Usuario.email.ilike(f"%{correo}%"))
    if telefono:
        consulta = consulta.filter(Usuario.telefono.ilike(f"%{telefono}%"))

    resultados = consulta.all()

    # Crear un DataFrame de pandas con los resultados
    data = {
        'Nombre': [usuario.nombre for usuario in resultados],
        'Apellidos': [usuario.apellidos for usuario in resultados],
        'Documento': [usuario.documentacion for usuario in resultados],
        'Edad': [usuario.edad for usuario in resultados],
        'Género': [usuario.genero for usuario in resultados],
        'Correo Electrónico': [usuario.email for usuario in resultados],
        'Teléfono': [usuario.telefono for usuario in resultados],
    }

    df = pd.DataFrame(data)

    # Crear un archivo Excel temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        excel_filename = temp_file.name
        df.to_excel(excel_filename, index=False)

    # Devolver el archivo Excel al usuario
    return send_file(excel_filename, as_attachment=True)

# Ruta para mostrar la lista temporal
@app.route('/lista', methods=['GET'])
def mostrar_lista():
    return render_template('lista.html', lista_temporal=lista_temporal)

# Ruta para generar el Excel desde la lista temporal
@app.route('/generar_excel_lista', methods=['GET'])
def generar_excel_lista():
    # Crear un DataFrame de pandas con los usuarios de la lista temporal
    data = {
        'Nombre': [usuario.nombre for usuario in lista_temporal],
        'Apellidos': [usuario.apellidos for usuario in lista_temporal],
        'Documento': [usuario.documentacion for usuario in lista_temporal],
        'Edad': [usuario.edad for usuario in lista_temporal],
        'Género': [usuario.genero for usuario in lista_temporal],
        'Correo Electrónico': [usuario.email for usuario in lista_temporal],
        'Teléfono': [usuario.telefono for usuario in lista_temporal],
    }

    df = pd.DataFrame(data)

    # Crear un archivo Excel temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        excel_filename = temp_file.name
        df.to_excel(excel_filename, index=False)

    # Devolver el archivo Excel al usuario
    return send_file(excel_filename, as_attachment=True)


@app.route('/agregar_a_lista/<int:id>', methods=['GET'])
def agregar_a_lista(id):
    usuario = Usuario.query.get(id)
    if usuario:
        lista_temporal.append(usuario)
    return redirect(url_for('mostrar_lista'))

@app.route('/borrar_lista_temporal', methods=['GET'])
def borrar_lista_temporal():
    # Lógica para borrar la lista temporal, por ejemplo, puedes borrar todos los registros de la lista temporal
    lista_temporal.clear()

    # Redirige a la página de la lista temporal después de borrar
    return redirect(url_for('index'))



# ... (otras importaciones y configuraciones)

@app.route('/bajausuarios', methods=['GET', 'POST'])
def bajausuarios():
    usuarios = Usuario.query.all()

    if request.method == 'POST':
        usuario_id = request.form['usuario_id']

        # Busca y borra el usuario por su ID
        usuario_a_borrar = Usuario.query.get(usuario_id)

        if usuario_a_borrar:
            db.session.delete(usuario_a_borrar)
            db.session.commit()

            # Puedes redirigir a una página de confirmación o a donde consideres
            return redirect(url_for('.index'))

    return render_template('bajausuarios.html', usuarios=usuarios)


if __name__ == '__main__':
    app.run(debug=True)