from flask import Flask

from flask import render_template, request, redirect,send_from_directory


#Conexion con Base de Datos en MySql

from flask_mysqldb import MySQL

#Importar Datetime

from datetime import datetime

import os

#Crear Aplicación

app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'sistema'

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA


# Creamos la ruta
@app.route('/index_destino')
def index_destino():

#Crear variable

    sql = "SELECT * FROM destinos;"

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql)
    db_destinos = cursor.fetchall()
    
    print("-"*60)
    for destino in db_destinos:
        print(destino)
        print("-"*60)
        
        cursor.close()

    return render_template ('viajes/index_destino.html', destinos=db_destinos)


# Funcion para eliminar un registro

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `sistema`.`destinos` WHERE id=%s", (id,))
    conn.commit()
    return redirect('/index_destino')

# Funcion para Editar un registro

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `sistema`.`destinos` WHERE id=%s", (id,))
    destinos = cursor.fetchall()
    cursor.close()
    conn.commit()
    return render_template('/viajes/edit.html', destinos=destinos)


#Funcion Update
@app.route('/update', methods=['POST'])
def update():

    _ciudad = request.form['txtCiudad']
    _pais = request.form['txtPais']
    _id = request.form['txtID']
    _foto = request.files['txtFoto']
    conn = mysql.connection
    cursor = conn.cursor()

    sql = "UPDATE sistema.destinos SET ciudad=%s, pais=%s WHERE id=%s"
    datos= (_ciudad, _pais,_id,)

    
    cursor.execute(sql, datos)
    
    if _foto.filename != '':
# Guardamos la foto con un nombre único basado en el tiempo
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)
# Consultamos la foto anterior para borrarla del servidor
        cursor.execute("SELECT foto FROM sistema.destinos WHERE id=%s", (_id,))

        fila = cursor.fetchone()
        if fila and fila[0] is not None:
                nombreFotoAnterior = fila[0]
                rutaFotoAnterior = os.path.join(app.config['CARPETA'],nombreFotoAnterior)
        if os.path.exists(rutaFotoAnterior):
            os.remove(rutaFotoAnterior)
    
        cursor.execute("UPDATE sistema.destinos SET foto=%s WHERE id=%s", (nuevoNombreFoto, _id))
    
    
    conn.commit()
    cursor.close()
    

    return redirect('/index_destino')

#Funcion Uploads

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)


# Creamos ruta para crear destinos

@app.route('/create')
def create():

    return render_template ('viajes/create.html')

#rutas para los htmls
@app.route('/')
def index():

    return render_template ('index.html')

@app.route('/destinos')
def destinos():

    return render_template ('destinos.html')

# Creamos ruta para storage

@app.route('/store', methods=['POST'])
def storage():

    _ciudad = request.form['txtCiudad']
    _pais = request.form['txtPais']
    _foto = request.files['txtFoto']
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if _foto.filename != '':
        nuevoNombreFoto= tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
    datos = (_ciudad, _pais, nuevoNombreFoto)
    
    
    sql = "INSERT INTO `sistema`.`destinos` (`id`, `ciudad`, `pais`, `foto`)\
        VALUES (NULL, %s, %s, %s);"

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    
 
    return redirect('/index_destino')
    
    



if __name__=='__main__':
    
    app.run(debug=True)
    
