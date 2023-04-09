from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL
import datetime, time

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "clinic"

mysql = MySQL(app)


@app.route("/")
def index():
    return redirect(url_for("pacientes"))


@app.route("/pacientes")
def pacientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pacientes")
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template("pacientes.html", patients=data)


@app.route("/agregar_paciente")
def agregar_paciente():
    return render_template("agregar-paciente.html")


@app.route("/cargar_paciente", methods=["POST"])
def cargar_paciente():
    if request.method == "POST":
        identificacion = request.form["identificacion"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        nacimiento = request.form["nacimiento"]
        contacto = request.form["contacto"]
        direccion = request.form["direccion"]
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO pacientes (identificacion, nombres, apellidos, nacimiento, contacto, direccion) VALUES (%s, %s, %s, %s, %s, %s)",
            (identificacion, nombres, apellidos, nacimiento, contacto, direccion),
        )
        mysql.connection.commit()
        print(identificacion)
        print(nombres)
        print(apellidos)
        print(nacimiento)
        print(contacto)
        print(direccion)
        cur.close()
        return redirect(url_for("pacientes"))


@app.route("/citas")
def citas():
    citas = [
        (1, "alejandro pacheco", (9, 00), (9, 45), "control", True),
        (2, "alex pacheco", (10, 15), (11, 00), "vacuna", False),
    ]
    print(citas)
    hours = citas[0][2]
    return render_template("citas.html", appointments=citas)


@app.route("/facturas")
def facturas():
    facturas = [
        ("Alex Pacheco", 122, (2023, 8, 3), 211000, 12, (2023, 8, 4), True),
        ("Alejandro Pacheco", 126, (2023, 6, 4), 92000, 12, (2023, 7, 5), False),
        ("Maria Hernandez", 128, (2023, 8, 4), 526500, 12, (2023, 8, 5), True),
    ]
    print(facturas)
    return render_template("facturas.html", checks=facturas)


@app.route("/listado")
def listado():
    return render_template("listado.html")


@app.route("/sesion")
def sesion():
    return render_template("sesion.html")


@app.route("/logout")
def logout():
    return "logout"


if __name__ == "__main__":
    app.run(debug=True)
