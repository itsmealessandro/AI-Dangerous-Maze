import search_element
import random


class maze:
    # la griglia è la mappa di gioco
    grid = []
    #variabili per selezionare quale griglia usare
    num_grid = 0
    grids = []

    # la posizione dell'agente è una coppia, il primo numero rappresenta l'asse X, il secondo l'asse Y
    agent_pos = 0, 0
    # posizione portale
    portal_target = 0, 0

    # metodo che serve a trovare le coordinate del portale
    def check_portal(self):
        posizione_T = search_element.trova_O(self.grid)
        if posizione_T:
            a, b = posizione_T
            return (a, b)
        else:
            return None

    def __init__(self):
        # "A": rappresenta la posizione dell'agente
        # "-": rappresenta una cella vuota esplorabile
        # "H": rappresenta un buco, se l'agente ci finisce sopra ricomincia da capo
        # "T": rappresenta il target, se l'agente ci finisce sopra vice
        # "P": rappresenta un portale che manderà l'agente sulla cella rappresentata dalla lettera "O"
        grid1 = [
            ["A", "-", "-", "-", "-", "-", "-", "-", "H", "O"],
            ["-", "H", "-", "-", "-", "-", "-", "H", "H", "-"],
            ["-", "-", "-", "H", "-", "P", "-", "-", "H", "T"]
        ]

        grid2 = [
            ["A", "-", "-", "-", "-", "-", "-", "-", "H", "O"],
            ["-", "H", "-", "-", "-", "-", "-", "H", "H", "-"],
            ["T", "-", "-", "-", "-", "P", "-", "-", "-", "-"]
        ]

        grid3 = [
            ["A", "-", "-", "-", "T", "-", "-", "-", "H", "O"],
            ["-", "H", "-", "-", "-", "-", "-", "H", "H", "-"],
            ["-", "-", "-", "H", "-", "P", "-", "-", "H", "-"]
        ]

        self.grids = [grid1, grid2, grid3]
        self.num_grid = random.randint(0, 2)
        self.grid = self.grids[self.num_grid]

        self.portal_target = self.check_portal()

    # funzione che viene chiamata alla fine di ogni episodio per resettare la mappa di gioco
    def reset(self):
        if self.num_grid == 0:
            self.grid = [
                ["A", "-", "-", "-", "-", "-", "-", "-", "H", "O"],
                ["-", "H", "-", "-", "-", "-", "-", "H", "H", "-"],
                ["-", "-", "-", "H", "-", "P", "-", "-", "H", "T"]
            ]
        elif self.num_grid == 1:
            self.grid = [
                ["A", "-", "-", "-", "-", "-", "-", "-", "H", "O"],
                ["-", "H", "-", "-", "-", "-", "-", "H", "H", "-"],
                ["T", "-", "-", "-", "-", "P", "-", "-", "-", "-"]
            ]
        elif self.num_grid == 2:
            self.grid = [
                ["A", "-", "-", "-", "T", "-", "-", "-", "H", "O"],
                ["-", "H", "-", "-", "-", "-", "-", "H", "H", "-"],
                ["-", "-", "-", "H", "-", "P", "-", "-", "H", "-"]
            ]
        self.agent_pos = 0, 0

    # ******************** Agent Movements ********************

    # metodo che raggruppa tutti i 4 movimenti possibili
    def agent_move(self, move):
        y = self.agent_pos[0]
        x = self.agent_pos[1]
        print("%s, posizione agente: %d %d" % (move, y, x))

        # controllo se il movimento fa uscire l'agente dalla mappa
        if move == "up" and y - 1 < 0:
            return "out"

        elif move == "down" and y + 1 > 2:
            return "out"

        elif move == "right" and x + 1 > 9:
            return "out"

        elif move == "left" and x - 1 < 0:
            return "out"

        # preparo le variabili relative alla futura posizione dell'agente
        if move == "up":
            newY = y - 1
            newX = x
        elif move == "down":
            newY = y + 1
            newX = x
        elif move == "right":
            newY = y
            newX = x + 1
        elif move == "left":
            newY = y
            newX = x - 1
        else:
            raise Exception("move ha un valore sbagliato")

        # controllo in che tipo di casella finirebbe l'agente una volta mosso
        if self.grid[newY][newX] == "H":
            return "hole"  # l'agente è caduto
        elif self.grid[newY][newX] == "T":
            return "win"  # l'agente ha vinto
        elif self.grid[newY][newX] == "P":

            # spostamento visivo dell'agente
            self.grid[y][x] = "-"
            a, b = self.portal_target
            self.grid[a][b] = "A"

            # rimuovo il portale visivamente
            self.grid[newY][newX] = "-"

            # segno lo spostamento nelle varaibili 
            self.agent_pos = a, b
            for j in range(3): print(self.grid[j])
            return "portal"

        # sposto l'agente visivamente        
        self.grid[y][x] = "-"
        self.grid[newY][newX] = "A"

        # segno lo spostamento nelle variabili
        self.agent_pos = newY, newX

        for j in range(3): print(self.grid[j])
        return move
