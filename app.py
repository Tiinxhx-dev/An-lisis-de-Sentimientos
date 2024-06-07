from flask import Flask, render_template, request, redirect, send_from_directory
from flask_mysqldb import MySQL
from datetime import datetime
import os

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'sistema'
app.config['UPLOAD_FOLDER'] = 'uploads/'
mysql.init_app(app) 


CARPETA = "uploads"
app.config["CARPETA"] = CARPETA





@app.route("/")
def index():
    sql = "SELECT * FROM empleados;"
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("USE sistema")
    cursor.execute(sql)
    
    empleados = cursor.fetchall()
    print(empleados)
    
    conn.commit()
    
    
    return render_template("empleados/index.html", empleados=empleados)

@app.route("/destroy/<int:id>", methods=["GET"] )
def destroy(id):
    conn = mysql.connect
    cursor = conn.cursor()
    
    cursor.execute("USE sistema")
    
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id,))
    fila = cursor.fetchone()
    os.remove(os.path.join(app.config["CARPETA"], fila[0]))
        
    
    cursor.execute("DELETE FROM empleados WHERE id=%s" ,(id,))
    conn.commit()
    return redirect("/") 


@app.route("/edit/<int:id>")
def edit(id):
    
    conn = mysql.connect
    cursor = conn.cursor()
    
    cursor.execute("USE sistema")
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id,))
    empleados = cursor.fetchall()
    conn.commit()
    print(empleados)
    return render_template("empleados/edit.html", empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]
    
    id = request.form["txtID"]
    
    sql = "UPDATE empleados SET nombre = %s, correo = %s WHERE id = %s;"
    datos = (_nombre, _correo, id)
    
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("USE sistema")
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if _foto.filename != "":
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save(os.path.join(app.config["CARPETA"], nuevoNombreFoto))
    
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id,))
        fila = cursor.fetchone()
        
        if fila and fila[0]:
            os.remove(os.path.join(app.config["CARPETA"], fila[0]))
        
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))
        conn.commit()
    
    cursor.execute(sql, datos)
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return redirect("/")

@app.route("/uploads/<nombreFoto>")
def uploads(nombreFoto):
    return send_from_directory(app.config["CARPETA"],nombreFoto)


@app.route('/create')
def create():
    return render_template("empleados/create.html")

@app.route("/store", methods=["POST"])
def storage():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    
    _foto = request.files["txtFoto"]
    
    now = datetime.now() 
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename != "":
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre,_correo,nuevoNombreFoto)
    conn = mysql.connect
    cursor = conn.cursor()   
    
    cursor.execute("USE sistema")
    cursor.execute(sql, datos)
    conn.commit()
    return redirect("/")
    



if __name__ == "__main__":
    app.run(debug=True)
    
    