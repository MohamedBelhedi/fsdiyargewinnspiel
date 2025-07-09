from flask import Flask, render_template, request, redirect, send_file, session, url_for
from io import StringIO
import csv

app = Flask(__name__)
app.secret_key = "dein_geheimes_passwort"  # Für Session-Login

datenbank = []  # Einfache In-Memory-Datenbank

# Hauptseite
@app.route("/", methods=["GET", "POST"])
def callIndex():
    search = request.form.get("search", "").strip().lower()
    return render_template("index.html", search=search)

# Gewinnspiel
@app.route("/gewinnspiel", methods=["GET", "POST"])
def gewinnSpiel():
    if request.method == "POST":
        eintrag = {
            "name": request.form.get("name", ""),
            "vorname": request.form.get("vorname", ""),
            "adresse": request.form.get("adresse", ""),
            "geburtsdatum": request.form.get("geb", ""),
            "geburtsort": request.form.get("gebo", ""),
            "gewinn": request.form.get("gewinn", "")
        }
        datenbank.append(eintrag)
        return redirect("/danke")
    return render_template("gewinnspiel.html")

@app.route("/danke")
def danke():
    return "Vielen Dank für deine Teilnahme!"

# Admin Login
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == "admin123":  # Einfaches Passwort, du kannst das erweitern
            session["admin"] = True
            return redirect("/admin")
        else:
            return render_template("admin_login.html", error="Falsches Passwort")
    return render_template("admin_login.html")

# Admin Panel (passwortgeschützt)
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin-login")
    return render_template("admin_panel.html", daten=datenbank)

# Daten als CSV exportieren
@app.route("/export")
def export():
    if not session.get("admin"):
        return redirect("/admin-login")
    if not datenbank:
        return "Keine Daten zum Exportieren vorhanden."
    si = StringIO()
    writer = csv.DictWriter(si, fieldnames=datenbank[0].keys())
    writer.writeheader()
    writer.writerows(datenbank)
    si.seek(0)
    return send_file(
        StringIO(si.getvalue()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='gewinner.csv'
    )

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)





