def trova_O(griglia):
    # Ciclo attraverso tutte le righe
    for indice_riga, riga in enumerate(griglia):
        # Ciclo attraverso tutte le colonne all'interno della riga corrente
        for indice_colonna, elemento in enumerate(riga):
            if elemento == "O":
                return (indice_riga, indice_colonna)
    # Se non viene trovato l'elemento "O", restituisci None
    print("non lo trovo")

def trova_A(griglia):
    # Ciclo attraverso tutte le righe
    for indice_riga, riga in enumerate(griglia):
        # Ciclo attraverso tutte le colonne all'interno della riga corrente
        for indice_colonna, elemento in enumerate(riga):
            if elemento == "A":
                return (indice_riga, indice_colonna)
    # Se non viene trovato l'elemento "T", restituisci None
    print("non lo trovo")