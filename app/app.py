from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mysqldb import MySQL
import datetime, time

app = Flask(__name__)


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "clinic"

mysql = MySQL(app)
app.secret_key = "mysecretkey"

""" VISTA DE PACIENTES """


@app.route("/")
def index():
    return redirect(url_for("pacientes"))


@app.route("/pacientes")
def pacientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pacientes")
    data = cur.fetchall()
    cur.close()
    return render_template("pacientes.html", patients=data)


@app.route("/paciente/<string:id>")
def paciente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pacientes where id = %s", id)
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template("detalle_paciente.html", patient=data)


## AGREGAR PACIENTES


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
        cur.close()
        return redirect(url_for("pacientes"))


## EDITAR PACIENTES


@app.route("/editar_paciente/<string:id>")
def editar_paciente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pacientes WHERE id = %s", id)
    data = cur.fetchall()
    cur.close()
    return render_template("guardar_edición_paciente.html", patient=data[0])


@app.route("/guardar_edicion_paciente/<string:id>", methods=["POST"])
def guardar_edicion_paciente(id):
    if request.method == "POST":
        identificacion = request.form["identificacion"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        nacimiento = request.form["nacimiento"]
        contacto = request.form["contacto"]
        direccion = request.form["direccion"]
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE pacientes
            SET identificacion = %s,
            nombres = %s,
            apellidos = %s,
            nacimiento = %s,
            contacto = %s,
            direccion = %s
            WHERE id = %s
        """,
            (identificacion, nombres, apellidos, nacimiento, contacto, direccion, id),
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("pacientes"))


## ELIMINAR PACIENTES


@app.route("/eliminar_paciente/<string:id>")
def eliminar_pacientes(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pacientes WHERE id = %s", id)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("pacientes"))


""" VISTA DE CITAS """


@app.route("/citas")
def citas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM citas")
    data = cur.fetchall()
    cur.execute("SELECT * FROM pacientes")
    patients = cur.fetchall()
    cur.close()
    print(data)
    # print(patients)
    return render_template("citas.html", appointments=data, patients=patients)


@app.route("/editar_cita/<string:id>", methods=["POST"])
def editar_cita(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM citas WHERE id = %s", id)
    data = cur.fetchall()
    cur.close()
    return render_template("editar_cita.html", cita=data)


@app.route("/agendar_cita")
def agregar_cita():
    return render_template("agendar_cita.html")


@app.route("/guardar_cita", methods=["POST"])
def guardar_cita():
    if request.method == "POST":
        ingreso = request.form["ingreso"]
        salida = request.form["salida"]
        paciente = request.form["paciente"]
        razon = request.form["razon"]
        email = request.form["email"]
        contacto = request.form["contacto"]
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO citas (ingreso, salida, paciente, razon, correo, contacto) VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (ingreso, salida, paciente, razon, email, contacto),
        )
        mysql.connection.commit()
        cur.close()
        flash("Cita guardada")
        return redirect(url_for("citas"))


@app.route("/detalle_cita/<string:id>")
def detalle_cita(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM citas WHERE id = %s", id)
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template("detalle_cita.html", appointment=data)


""" VISTA FACTURAS """


@app.route("/facturas")
def facturas():
    facturas = [
        ("Alex Pacheco", 122, (2023, 8, 3), 211000, 12, (2023, 8, 4), True),
        ("Alejandro Pacheco", 126, (2023, 6, 4), 92000, 12, (2023, 7, 5), False),
        ("Maria Hernandez", 128, (2023, 8, 4), 526500, 12, (2023, 8, 5), True),
    ]
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
