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


# =============================================
# STUDENTE C - pagina 5
# =============================================

if __name__ == "__main__":
    app.run(debug=True)
