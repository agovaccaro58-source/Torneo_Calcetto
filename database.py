#Importa il driver di mysql per permettere a python di comunicare con il database
import mysql.connector

#definisce la funzione per stabilire e restituire una connessione al database di mysql
def connetti():
    #restituisce l'oggetto di connessione configurato con i parametri del server locale
    return mysql.connector.connect(

        host="localhost", #indirizzo del server del databse locale
        user="root",    #nome utente del database
        password="Vivaletette05/",   #password per entrare al database
        database="calcetto",   #il database a cui ci connettiamo


    )

#definisce la funzione per calcolare e recuperare la classifica generale del torneo
def query_classifica():
    conn = connetti() #apre la connessione al database
    cursor = conn.cursor(dictionary=True) #crea un cursore che restituisce i risultati come dizionari (chiave:valore)
    # Copia qui la query fornita in fondo al file calcetto.sql
    # Assicurati che nella SELECT ci sia s.id_squadra
    #esegue la query sql avanzata per calcolare le statistiche di ogni squadra
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
    risultato = cursor.fetchall() #recupera tutte le righe restituite dalla query
    cursor.close() #chiude il cursore
    conn.close() #chiude la connessione al database
    return risultato #restituisce i dati della classifica

#definisce la funzione pe recuperare le prossime 3 partite in programma
def query_prossime_partite():
    conn = connetti() #apre la connessione al database
    cursor = conn.cursor(dictionary=True) #crea il cursore in modalità dizionario
    #query per selezionare le prossime partite non ancora giocate
    cursor.execute("""
        SELECT p.data_ora, p.campo, sc.nome AS casa, so.nome AS ospite
        FROM partite p
        JOIN squadre sc ON sc.id_squadra = p.id_squadra_casa
        JOIN squadre so ON so.id_squadra = p.id_squadra_ospite
        WHERE p.gol_casa IS NULL
        ORDER BY p.data_ora
        LIMIT 3
    """)
    risultato = cursor.fetchall() #recupera tutte 3 le righe
    cursor.close()  #chiude il cursore
    conn.close() #chiude la connessione al databse
    return risultato #restituisce le prossime partite

#definisce la funzione per ottenere l'elenco delle squadre con il rispettivo numero di giocatori
def query_squadre_con_numero_giocatori():
    conn = connetti() #apre la connessione al databse
    cursor = conn.cursor(dictionary=True) #crea il cursore in modalità dizionario
    #query per contare i giocatori registrati per ciascuna squadra
    cursor.execute("""
        SELECT s.id_squadra, s.nome, s.colore_maglia, s.responsabile, COUNT(g.id_giocatore) AS num_giocatori
        FROM squadre s
        LEFT JOIN giocatori g ON s.id_squadra = g.id_squadra
        GROUP BY s.id_squadra, s.nome, s.colore_maglia, s.responsabile
        ORDER BY s.nome
    """)
    risultato = cursor.fetchall() #recupera tutte le righe dei risultati
    cursor.close() #chiude il cursore
    conn.close() #chiude la connessione
    return risultato #restituisce l'elenco delle squadre

#definisce la funzione per recuperare le informazioni di una specifica squadra tramite ID
def query_squadra(id_squadra):
    """Restituisce i dati anagrafici di una singola squadra."""
    conn = connetti() #apre la connessione
    cursor = conn.cursor(dictionary=True) #crea il cursore in modalità dizionario
    #query parametrizzata per evitare sql injection
    cursor.execute(
        """
        SELECT id_squadra, nome, colore_maglia, responsabile
        FROM squadre
        WHERE id_squadra = %s
    """,
        (id_squadra,),
    )
    risultato = cursor.fetchone()  # Una sola riga (o None se non esiste)
    cursor.close()
    conn.close()
    return risultato

#definisce la funzione per recuperare l'elenco dei giocatori di una determinata squadra
def query_giocatori_squadra(id_squadra):
    """Restituisce la rosa della squadra ordinata per numero di maglia."""
    conn = connetti() #apre la connessione
    cursor = conn.cursor(dictionary=True) #crea il cursore in modalità dizionario
    #query per selezionare i giocatori filtrati per squadre
    cursor.execute(
        """
        SELECT numero_maglia, nome, cognome, ruolo
        FROM giocatori
        WHERE id_squadra = %s
        ORDER BY numero_maglia ASC
    """,
        (id_squadra,),  #un parametro sicuro per id squadra
    )
    risultato = cursor.fetchall() #recupera tutti i giocatori della squadra
    cursor.close() #chiude il cursore
    conn.close() #chiude la connessione
    return risultato #restituisce la rosa dei giocatori


#definisce la funzione per recuperare lo storico partite di una singola squadra
def query_partite_squadra(id_squadra):
    """Restituisce le partite disputate o da disputare da una squadra (sia in casa che fuori)."""
    conn = connetti() #apre la connessione
    cursor = conn.cursor(dictionary=True) #crea il cursore in modalità dizionario
    #query per recuperare le partite in cui la squadra gioca in casa o in trasferta
    cursor.execute(
        """
        SELECT p.giornata, p.data_ora, p.campo,
               sc.nome AS casa, so.nome AS ospite,
               p.gol_casa, p.gol_ospite
        FROM partite p
        JOIN squadre sc ON sc.id_squadra = p.id_squadra_casa
        JOIN squadre so ON so.id_squadra = p.id_squadra_ospite
        WHERE p.id_squadra_casa = %s OR p.id_squadra_ospite = %s
        ORDER BY p.giornata ASC, p.data_ora ASC
    """,
        (id_squadra, id_squadra), #passa l'id due volte (casa e ospite)
    )
    risultato = cursor.fetchall() #recupera l'elenco delle partite
    cursor.close() #chiude il cursore
    conn.close() #chiude la connessione
    return risultato #restituisce le partite della squadra


#definsice la funzione per recuperare l'intero calendario del torneo
def query_calendario():
    """Restituisce tutte le partite del torneo ordinate per giornata e ora."""
    conn = connetti() #apre la connessione
    cursor = conn.cursor(dictionary=True) #crea il cursore in modalità dizionario
    #query completa per ottenere la lista completa di tutte le partite
    cursor.execute("""
        SELECT p.giornata, p.data_ora, p.campo,
               sc.nome AS casa, so.nome AS ospite,
               p.gol_casa, p.gol_ospite
        FROM partite p
        JOIN squadre sc ON sc.id_squadra = p.id_squadra_casa
        JOIN squadre so ON so.id_squadra = p.id_squadra_ospite
        ORDER BY p.giornata ASC, p.data_ora ASC
    """)
    risultato = cursor.fetchall() #recupera l'intero claendario
    cursor.close() #chiude il cursore
    conn.close() #chiude la connessione
    return risultato #restituisce l'intero calendario


#definisce la funzione per calcolare le statistiche generali del torneo
def query_numeri_torneo():
    conn = connetti() #apre la connessionoe
    cursor = conn.cursor(dictionary=True) #il cursore in modalità dizionario
    #query di aggregazione su partite disputate, goal totali e media goal a partita
    cursor.execute("""
        SELECT 
            COUNT(*) AS giocate,
            SUM(gol_casa + gol_ospite) AS gol_totali,
            ROUND(AVG(gol_casa + gol_ospite), 2) AS media_gol
        FROM partite
        WHERE gol_casa IS NOT NULL
    """)
    risultato = cursor.fetchone() #recupera la singola riga di riepilogo
    cursor.close() #chiude il cursore
    conn.close() #chiude la connessione
    return risultato #restituisce le statistiche generali


#definisce la funzione per generare la classifica marcatori (marcatori con più reti)
def query_classifica_marcatori():
    conn = connetti() #apre la connessione
    cursor = conn.cursor(dictionary=True) #crea il cursore in modalità dizionario
    #query per calcolare quanti goal ha segnato ogni giocatore
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
    risultato = cursor.fetchall() #recupera l'elenco dei marcatori
    cursor.close() #chiude il curosre
    conn.close() #termina la cnnessione
    return risultato #riporta la classifica dei marcatori


#definisce la funzione per trovare la partita con il maggior numero di goal
def query_partita_piu_gol():
    conn = connetti() #apre la connessione
    cursor = conn.cursor(dictionary=True) #crea il cursore in modalità dizionario
    #query per calcolare la somma dei goal in ogni partita e trovare quella con più punteggio
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
    risultato = cursor.fetchone() #recupera l'unica riga del risultato
    cursor.close() #chiude il cursore
    conn.close() #chiude la connessione
    return risultato #restituisce la partita con più goal