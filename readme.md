# Torneo di Calcetto - Web App

Sito web di consultazione per il torneo di calcetto a 6 squadre. Permette a giocatori e tifosi di visualizzare classifica, rose, calendario delle partite e statistiche sui marcatori.

---

## 🗄️ Database (`calcetto`)

Il database è composto da 4 tabelle principali:
- **`squadre`**: `id_squadra`, `nome`, `colore_maglia`, `responsabile`
- **`giocatori`**: `id_giocatore`, `id_squadra`, `nome`, `cognome`, `numero_maglia`, `ruolo`
- **`partite`**: `id_partita`, `giornata`, `id_squadra_casa`, `id_squadra_ospite`, `data_ora`, `campo`, `gol_casa`, `gol_ospite`
- **`gol`**: `id_gol`, `id_partita`, `id_giocatore`, `minuto`

---

## 🌐 Struttura delle Pagine e Suddivisione del Lavoro

| Pagina | Indirizzo | Descrizione | Responsabile |
| :--- | :--- | :--- | :--- |
| **Pagina 1** | `/` | Classifica generale e card con le prossime 3 partite | Studente A |
| **Pagina 2** | `/squadre` | Elenco di tutte le squadre con numero dei giocatori | Studente A |
| **Pagina 3** | `/squadra/<id>` | Scheda dettagliata della squadra, rosa e storico partite | Studente B |
| **Pagina 4** | `/calendario` | Calendario completo delle 5 giornate con i risultati | Studente B |
| **Pagina 5** | `/marcatori` | Statistiche torneo, classifica marcatori e partita con più gol | Studente C |

---

## 🛠️ Tecnologie Utilizzate

- **Backend:** Python con Framework **Flask**
- **Database:** **MySQL** / MariaDB (connettore `mysql-connector-python`)
- **Template Engine:** **Jinja2**
- **Frontend & Styling:** **Bootstrap 5** + CSS personalizzato (`static/style.css`)cd