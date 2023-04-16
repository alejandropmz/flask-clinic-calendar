from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import datetime, time

app = Flask(__name__)
Bootstrap(app)


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
    if data:
        cur.close()
        return render_template("pacientes.html", patients=data)
    return render_template("no_disponible.html", mensaje="pacientes")


## DETALLE PACIENTE


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
        correo = request.form["correo"]
        direccion = request.form["direccion"]
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO pacientes (identificacion, nombres, apellidos, nacimiento, contacto, correo, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                identificacion,
                nombres,
                apellidos,
                nacimiento,
                contacto,
                correo,
                direccion,
            ),
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("pacientes"))


## EDITAR PACIENTES


@app.route("/editar_paciente/<string:id>", methods=["GET", "POST"])
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
    if data:
        cur.execute(
            """
        SELECT citas.*, pacientes.nombres, pacientes.apellidos
        FROM citas
        JOIN pacientes ON citas.paciente = pacientes.id
    """
        )
        complete_data = cur.fetchall()
        cur.close()
        print(complete_data)
        return render_template("citas.html", complete_data=complete_data)
    return render_template("no_disponible.html", mensaje="Citas")


""" @app.route("/citas")
def citas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM citas")
    data = cur.fetchall()
    if data:
        cur.execute("SELECT * FROM pacientes WHERE id = %s", (data[0][4],))
        patients = cur.fetchall()
        cur.close()
        # print(data)
        print(patients)
        # fecha = data[0][2]
        # print(str(fecha))
        return render_template("citas.html", appointments=data, patients=patients)
    return render_template("no_disponible.html", mensaje="Citas") """


@app.route("/editar_cita/<string:id>", methods=["POST"])
def editar_cita(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM citas WHERE id = %s", id)
    data = cur.fetchall()
    cur.close()
    return render_template("editar_cita.html", cita=data)


@app.route("/agendar_cita")
def agregar_cita():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pacientes")
    data = cur.fetchall()
    cur.close()
    return render_template("agendar_cita.html", patients=data)


@app.route("/guardar_cita", methods=["POST"])
def guardar_cita():
    if request.method == "POST":
        fecha = request.form["fecha"]
        ingreso = request.form["ingreso"]
        salida = request.form["salida"]
        paciente = request.form["paciente"]
        razon = request.form["razon"]
        estado = True
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO citas (fecha, ingreso, salida, paciente, razon, estado) VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (fecha, ingreso, salida, paciente, razon, estado),
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
    print(data[0][3])

    cur2 = mysql.connection.cursor()
    if data is True:
        cur2.execute("SELECT * FROM pacientes WHERE id = %s", (data[0][4],))
        patient = cur2.fetchall()
        cur2.close()
        print(patient)
        return render_template("detalle_cita.html", appointment=data, patient=patient)


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
