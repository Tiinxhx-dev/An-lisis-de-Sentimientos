from flask import Flask, render_template
from flask_mysqldb import MySQL



app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'sistema'
mysql.init_app(app)


@app.route("/")
def index():
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Martin', 'martingal@gmail.com', 'foto.jpg');"
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("USE sistema")
    cursor.execute(sql)
    conn.commit()
    return render_template("empleados/index.html")


@app.route('/create')
def create():
    
    return render_template("empleados/create.html")





if __name__ == "__main__":
    app.run(debug=True)
    
    https://www.youtube.com/watch?v=gUED5uFmyQI