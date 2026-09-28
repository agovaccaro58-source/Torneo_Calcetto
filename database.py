def query_numeri_torneo():
    conn = connetti()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            COUNT(*) AS giocate,
            SUM(gol_casa + gol_ospite) AS gol_totali,
            ROUND(AVG(gol_casa + gol_ospite), 2) AS media_gol
        FROM partite
        WHERE gol_casa IS NOT NULL
    """)
    risultato = cursor.fetchone()
    cursor.close()
    conn.close()
    return risultato


def query_classifica_marcatori():
    conn = connetti()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            g.nome, 
            g.cognome, 
            s.nome AS squadra, 
            COUNT(gol.id_gol) AS reti
        FROM gol
        JOIN giocatori g ON g.id_giocatore = gol.id_giocatore
        JOIN squadre s ON s.id_squadra = g.id_squadra
        GROUP BY g.id_giocatore, g.nome, g.cognome, s.nome
        ORDER BY reti DESC, g.cognome ASC
    """)
    risultato = cursor.fetchall()
    cursor.close()
    conn.close()
    return risultato


def query_partita_piu_gol():
    conn = connetti()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            sc.nome AS casa, 
            so.nome AS ospite, 
            p.gol_casa, 
            p.gol_ospite,
            (p.gol_casa + p.gol_ospite) AS totale_gol
        FROM partite p
        JOIN squadre sc ON sc.id_squadra = p.id_squadra_casa
        JOIN squadre so ON so.id_squadra = p.id_squadra_ospite
        WHERE p.gol_casa IS NOT NULL
        ORDER BY totale_gol DESC
        LIMIT 1
    """)
    risultato = cursor.fetchone()
    cursor.close()
    conn.close()
    return risultato