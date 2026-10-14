# Torneo di Calcetto - Web App

Sito web di consultazione per la gestione del torneo di calcetto a 6 squadre.

## Struttura del Database (`calcetto`)
- **squadre**: `id_squadra`, `nome`, `colore_maglia`, `responsabile`
- **giocatori**: `id_giocatore`, `id_squadra`, `nome`, `cognome`, `numero_maglia`, `ruolo`
- **partite**: `id_partita`, `giornata`, `id_squadra_casa`, `id_squadra_ospite`, `data_ora`, `campo`, `gol_casa`, `gol_ospite`
- **gol**: `id_gol`, `id_partita`, `id_giocatore`, `minuto`

## Architettura e Pagine
- **Pagina 1 (`/`)**: Classifica + Prossime Partite (Studente A)
- **Pagina 2 (`/squadre`)**: Elenco delle squadre (Studente A)
- **Pagina 3 (`/squadra/<id>`)**: Scheda della singola squadra (Studente B)
- **Pagina 4 (`/calendario`)**: Calendario e risultati delle partite (Studente B)
- **Pagina 5 (`/marcatori`)**: Statistiche torneo, classifica marcatori e partita con più gol (Studente C)