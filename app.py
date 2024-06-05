from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import datetime


app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'sistema'
app.config['UPLOAD_FOLDER'] = 'uploads/'
mysql.init_app(app) 


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
    return render_template("empleados/index.html")


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
        _foto.save("uploads/+nuevoNombreFoto")
    
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre,_correo,nuevoNombreFoto)
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("USE sistema")
    cursor.execute(sql, datos)
    conn.commit()
    return render_template("empleados/index.html")
    



if __name__ == "__main__":
    app.run(debug=True)
    
    