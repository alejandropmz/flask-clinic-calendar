from flask import Flask, render_template

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
    return "citas"

@app.route("/facturas")
def facturas():
    return "facturas"

@app.route("/listado")
def listado():
    return "listado"

@app.route("/sesion")
def sesion():
    return "sesion"

@app.route("/logout")
def logout():
    return "logout"


if __name__ == '__main__':
    app.run(debug=True)