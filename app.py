from flask import Flask, render_template
import database

app = Flask(__name__)

# =============================================
# STUDENTE A - pagine 1 e 2
# =============================================


@app.route("/")
def index():
    classifica = database.query_classifica()
    prossime = database.query_prossime_partite()
    return render_template(
        "index.html", classifica=classifica, prossime=prossime
    )


@app.route("/squadre")
def squadre():
    squadre = database.query_squadre_con_numero_giocatori()
    return render_template("pagina2.html", squadre=squadre)


# =============================================
# STUDENTE B - pagine 3 e 4
# =============================================
@app.route("/squadra/<int:id_squadra>")
def dettaglio_squadra(id_squadra):
    squadra = database.query_squadra(id_squadra)
    if not squadra:
        return "Squadra non trovata", 404

    rosa = database.query_giocatori_squadra(id_squadra)
    partite = database.query_partite_squadra(id_squadra)

    return render_template(
        "pagina3.html", squadra=squadra, rosa=rosa, partite=partite
    )


@app.route("/partite")
def tutte_le_partite():
    partite = database.query_calendario()
    return render_template("pagina4.html", partite=partite)


# =============================================
# STUDENTE C - pagina 5
# =============================================


@app.route("/marcatori")
def marcatori():
    numeri = database.query_numeri_torneo()
    classifica_marcatori = database.query_classifica_marcatori()
    partita_top = database.query_partita_piu_gol()

    return render_template(
        "pagina5.html",
        numeri=numeri,
        marcatori=classifica_marcatori,
        partita_top=partita_top,
    )


if __name__ == "__main__":
    app.run(debug=True)
