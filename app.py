from flask import Flask, render_template, request, redirect, session
import sqlite3
from model import predict_disease

app = Flask(__name__)
app.secret_key = "project_secret"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    if "user" in session:
        return redirect("/predict")
    return redirect("/login")


@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        conn.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username,password)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/predict")

    return render_template("login.html")


@app.route("/predict", methods=["GET","POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    disease = None
    medicine = None

    if request.method == "POST":
        symptoms = request.form["symptoms"]
        disease, medicine = predict_disease(symptoms)

    return render_template("predict.html", disease=disease, medicine=medicine)


# ---------------- ADMIN ROUTE ----------------

@app.route("/admin")
def admin():
    if "user" not in session or session["user"] != "admin":
        return "Access Denied"

    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()

    return render_template("admin.html", users=users)

# ------------------------------------------------


@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)