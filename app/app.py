from flask import Flask, render_template
import datetime, time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/pacientes")
def pacientes():
    patients = [
        (1, "alejandro pacheco", (1997,24,11), "no tiene"),
        (1, "alex pacheco", (1997,24,11), "no tiene")
    ]
    return render_template('pacientes.html', info=patients)

@app.route("/citas")
def citas():
    citas = [
        (1, "alejandro pacheco", (9,00), (9, 45), "control", True),
        (2, "alex pacheco", (10, 15), (11,00), "vacuna", False)
    ]
    print(citas)
    hours = citas[0][2]
    return render_template('citas.html', appointments=citas)

@app.route("/facturas")
def facturas():
    facturas = [
        ("Alex Pacheco", 122, (2023, 8, 3), 211000, 12, (2023, 8, 4), True),
        ("Alejandro Pacheco", 126, (2023, 6, 4), 92000, 12, (2023, 7, 5), False),
        ("Maria Hernandez", 128, (2023, 8, 4), 526500, 12, (2023, 8, 5), True)
    ]
    print(facturas)
    return render_template('facturas.html', checks=facturas)

@app.route("/listado")
def listado():
    return render_template('listado.html')

@app.route("/sesion")
def sesion():
    return "sesion"

@app.route("/logout")
def logout():
    return "logout"


if __name__ == '__main__':
    app.run(debug=True)