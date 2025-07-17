from flask import Flask, render_template, request, redirect, send_file, session, url_for
from io import StringIO, BytesIO
import datetime as dt
import csv

app = Flask(__name__)
app.secret_key = "DiyarSito2022#"  # Für Session-Login

datenbank = []  # In-Memory-Datenbank
aktionsEnde = None  # Enddatum für die Aktion


@app.route("/gewinnspiel", methods=["GET", "POST"])
def gewinnSpiel():
    global aktionsEnde
    heute = dt.date.today()

    # Wenn das Gewinnspiel beendet ist, weiterleiten
    if aktionsEnde and heute > aktionsEnde:
        # return redirect("/aktionvorbei")
        return render_template("vorbeigewinnspiel.html")
    if request.method == "POST":
        eintrag = {
            "name": request.form.get("name", ""),
            "vorname": request.form.get("vorname", ""),
            "adresse": request.form.get("adresse", ""),
            "telefon": request.form.get("telefon", ""),
            "geburtsdatum": request.form.get("geb", ""),
            "geburtsort": request.form.get("gebo", ""),
            "gewinn": request.form.get("gewinn", "")
        }
        datenbank.append(eintrag)
        return redirect("/danke")

    return render_template("gewinnspiel.html", aktionsEnde=aktionsEnde)


@app.route("/danke")
def danke():
    return "Vielen Dank für deine Teilnahme!"


@app.route("/aktionvorbei")
def aktion_vorbei():
    return "Die Aktion ist leider abgelaufen."


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    global aktionsEnde
    error = None

    if request.method == "POST":
        dateEnd = request.form.get("dateEnde", "")
        try:
            aktionsEnde = dt.datetime.strptime(dateEnd, "%Y-%m-%d").date()
        except ValueError:
            error = "Ungültiges Datum"

        password = request.form.get("password", "")
        if password == "DiyarSito2022#":
            session["admin"] = True
            return redirect("/admin")
        else:
            error = error or "Falsches Passwort"
            return render_template("admin_login.html", error=error)

    return render_template("admin_login.html")


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin-login")
    return render_template("admin_panel.html", daten=datenbank, aktionsEnde=aktionsEnde)


@app.route("/export")
def export():
    if not session.get("admin"):
        return redirect("/admin-login")
    if not datenbank:
        return "Keine Daten zum Exportieren vorhanden."

    string_buffer = StringIO()
    writer = csv.DictWriter(string_buffer, fieldnames=datenbank[0].keys())
    writer.writeheader()
    writer.writerows(datenbank)

    byte_buffer = BytesIO()
    byte_buffer.write(string_buffer.getvalue().encode("utf-8"))
    byte_buffer.seek(0)

    return send_file(
        byte_buffer,
        mimetype="text/csv",
        as_attachment=True,
        download_name="gewinner_aktions.csv"
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/gewinnspiel")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
