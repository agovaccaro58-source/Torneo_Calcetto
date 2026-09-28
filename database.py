def query_classifica():
    conn = connetti()
    cursor = conn.cursor(dictionary=True)
    # Copia qui la query fornita in fondo al file calcetto.sql
    # Assicurati che nella SELECT ci sia s.id_squadra
    cursor.execute("""
        SELECT s.id_squadra, s.nome, 
               COUNT(p.id_partita) AS giocate,
               SUM(CASE WHEN (p.id_squadra_casa = s.id_squadra AND p.gol_casa > p.gol_ospite) OR (p.id_squadra_ospite = s.id_squadra AND p.gol_ospite > p.gol_casa) THEN 1 ELSE 0 END) AS vinte,
               SUM(CASE WHEN p.gol_casa = p.gol_ospite THEN 1 ELSE 0 END) AS pareggiate,
               SUM(CASE WHEN (p.id_squadra_casa = s.id_squadra AND p.gol_casa < p.gol_ospite) OR (p.id_squadra_ospite = s.id_squadra AND p.gol_ospite < p.gol_casa) THEN 1 ELSE 0 END) AS perse,
               SUM(CASE WHEN p.id_squadra_casa = s.id_squadra THEN p.gol_casa ELSE p.gol_ospite END) AS gol_fatti,
               SUM(CASE WHEN p.id_squadra_casa = s.id_squadra THEN p.gol_ospite ELSE p.gol_casa END) AS gol_subiti,
               (SUM(CASE WHEN p.id_squadra_casa = s.id_squadra THEN p.gol_casa ELSE p.gol_ospite END) - SUM(CASE WHEN p.id_squadra_casa = s.id_squadra THEN p.gol_ospite ELSE p.gol_casa END)) AS differenza,
               SUM(CASE 
                   WHEN (p.id_squadra_casa = s.id_squadra AND p.gol_casa > p.gol_ospite) OR (p.id_squadra_ospite = s.id_squadra AND p.gol_ospite > p.gol_casa) THEN 3
                   WHEN p.gol_casa = p.gol_ospite THEN 1
                   ELSE 0 
               END) AS punti
        FROM squadre s
        JOIN partite p ON s.id_squadra = p.id_squadra_casa OR s.id_squadra = p.id_squadra_ospite
        WHERE p.gol_casa IS NOT NULL
        GROUP BY s.id_squadra, s.nome
        ORDER BY punti DESC, differenza DESC, gol_fatti DESC
    """)
    risultato = cursor.fetchall()
    cursor.close()
    conn.close()
    return risultato

def query_prossime_partite():
    conn = connetti()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.data_ora, p.campo, sc.nome AS casa, so.nome AS ospite
        FROM partite p
        JOIN squadre sc ON sc.id_squadra = p.id_squadra_casa
        JOIN squadre so ON so.id_squadra = p.id_squadra_ospite
        WHERE p.gol_casa IS NULL
        ORDER BY p.data_ora
        LIMIT 3
    """)
    risultato = cursor.fetchall()
    cursor.close()
    conn.close()
    return risultato

def query_squadre_con_numero_giocatori():
    conn = connetti()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.id_squadra, s.nome, s.colore_maglia, s.responsabile, COUNT(g.id_giocatore) AS num_giocatori
        FROM squadre s
        LEFT JOIN giocatori g ON s.id_squadra = g.id_squadra
        GROUP BY s.id_squadra, s.nome, s.colore_maglia, s.responsabile
        ORDER BY s.nome
    """)
    risultato = cursor.fetchall()
    cursor.close()
    conn.close()
    return risultato