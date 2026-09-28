@app.route("/marcatori")
def marcatori():
    numeri = database.query_numeri_torneo()
    classifica_marcatori = database.query_classifica_marcatori()
    partita_spettacolo = database.query_partita_piu_gol()

    return render_template(
        "pagina5.html",
        numeri=numeri,
        marcatori=classifica_marcatori,
        partita_top=partita_spettacolo
    )