class maze:
    
    # la griglia è la mappa di gioco
    grid =[]

    # la posizione dell'agente è una coppia, il primo numero rappresenta l'asse X, il secondo l'asse Y
    agent_pos = 0,0

    def __init__(self):
        # "A": rappresenta la posizione dell'agente
        # "-": rappresenta una cella vuota esplorabile
        # "H": rappresenta un buco, se l'agente ci finisce sopra ricomincia da capo
        # "T": rappresenta il target, se l'agente ci finisce sopra vice
        # "P": rappresenta un portale che manderà l'agente sulla cella rappresentata dalla lettera "O"
        # "D": rappresenta una porta inizialmente chiuse, che si potrà aprire se l'agente finirà sulla cella "K" (chiave) 

        # per vincere l'agente dovrà necessariamente andare sulla chiave per aprire la porta del portale che gli permetterà di vincere

        self.grid =  [
            ["A","-","-","H","-","H","-","-","H","O"],
            ["-","H","-","K","-","-","-","H","H","-"],
            ["-","-","-","H","-","-","D","P","H","T"]
            ]
    
    # funzione che viene chiamata alla fine di ogni episodio per resettare la mappa di gioco
    def reset(self):
        self.grid =  [
            ["A","-","-","H","-","H","-","-","H","O"],
            ["-","H","-","K","-","-","-","H","H","-"],
            ["-","-","-","H","-","-","D","P","H","T"]
            ]
        self.agent_pos = 0,0
    
    # ******************** Agent Movements ********************
    def A_move_up(self):
        y = self.agent_pos[0]
        x = self.agent_pos[1]
        print("up, posizione agente: %d %d" %(y,x))
        
        # controllo se il movimento fa uscire l'agente dalla mappa
        if y -1 < 0:
            return "out"
        # l'agente è caduto

        elif self.grid[y-1][x] == "H":
            return "hole"
        # l'agente ha vinto

        elif self.grid[y-1][x] == "T":
            return "win"
        
        # l'agente è entrato nel portale
        elif self.grid[y-1][x] == "P":
            self.grid[y][x] = "-" 
            self.grid[1][2] = "A" 
            self.agent_pos = 0,9
            return "portal"
        
        elif self.grid[y-1][x] == "D":
            return "door"
        
        elif self.grid[y-1][x] == "K":
            # sposto l'agente visivamente
            self.grid[y][x] = "-" 
            self.grid[y-1][x] = "A" 
            # segno lo spostamento nelle variabili
            self.agent_pos = y-1,x

            # segno l'apertura della porta
            self.grid[2][6] = "-"
            return "key"
        
        
        # sposto l'agente visivamente
        for j in range(3): print(self.grid[j])
        print("----------")
        self.grid[y][x] = "-"
        self.grid[y-1][x] = "A" 
        # segno lo spostamento nelle variabili
        self.agent_pos = y-1,x
        for j in range(3): print(self.grid[j])
        return "up"

    def A_move_down(self):

        y = self.agent_pos[0]
        x = self.agent_pos[1]
        print("down, posizione agente: %d %d" %(y,x))
        if y +1 > 2:
            return "out"
        
        elif self.grid[y+1][x] == "H":
            return "hole"
        
        elif self.grid[y+1][x] == "T":
            return "win"
        
        elif self.grid[y+1][x] == "P":
            self.grid[y][x] = "-" 
            self.grid[1][2] = "A" 
            self.agent_pos = 0,9
            return "portal"
        
        elif self.grid[y+1][x] == "D":
            return "door"
        
        elif self.grid[y+1][x] == "K":
            # sposto l'agente visivamente
            self.grid[y][x] = "-" 
            self.grid[y+1][x] = "A" 
            # segno lo spostamento nelle variabili
            self.agent_pos = y+1,x

            # segno l'apertura della porta
            self.grid[2][6] = "-"
            return "key"
        
        # sposto l'agente visivamente
        for j in range(3): print(self.grid[j])
        print("----------")
        self.grid[y][x] = "-" 
        self.grid[y+1][x] = "A" 
        # segno lo spostamento nelle variabili
        self.agent_pos = y+1,x
        for j in range(3): print(self.grid[j])
        return "down"
    
    def A_move_right(self):
        y = self.agent_pos[0]
        x = self.agent_pos[1]
        print("right, posizione agente: %d %d" %(y,x))
        if x+1 > 2:
            return "out"
        
        elif self.grid[y][x+1] == "H":
            return "hole"
        
        elif self.grid[y][x+1] == "T":
            return "win"
        
        elif self.grid[y][x+1] == "P":
            self.grid[y][x] = "-" 
            self.grid[1][2] = "A" 
            self.agent_pos = 0,9
            return "portal"
        
        elif self.grid[y][x+1] == "D":
            return "door"
        
        elif self.grid[y][x+1] == "K":
            # sposto l'agente visivamente
            self.grid[y][x] = "-" 
            self.grid[y][x+1] = "A" 
            # segno lo spostamento nelle variabili
            self.agent_pos = y+1,x

            # segno l'apertura della porta
            self.grid[2][6] = "-"
            return "key"

        # sposto l'agente visivamente
        for j in range(3): print(self.grid[j])
        print("----------")
        self.grid[y][x] = "-" 
        self.grid[y][x+1] = "A" 
        # segno lo spostamento nelle variabili
        self.agent_pos = y,x+1
        for j in range(3): print(self.grid[j])
        return "right"

    def A_move_left(self):
        y = self.agent_pos[0]
        x = self.agent_pos[1]
        print("left, posizione agente: %d %d" %(y,x))
        if x-1 < 0:
            return "out"
        elif self.grid[y][x-1] == "H":
            return "hole"
        
        elif self.grid[y][x-1] == "T":
            return "win"
        
        elif self.grid[y][x-1] == "P":
            self.grid[y][x] = "-" 
            self.grid[1][2] = "A" 
            self.agent_pos = 0,9
            return "portal"
        
        elif self.grid[y][x-1] == "D":
            return "door"
        
        elif self.grid[y][x-1] == "K":
            # sposto l'agente visivamente
            self.grid[y][x] = "-" 
            self.grid[y][x-1] = "A" 
            # segno lo spostamento nelle variabili
            self.agent_pos = y+1,x

            # segno l'apertura della porta
            self.grid[2][6] = "-"
            return "key"

        # sposto l'agente visivamente
        for j in range(3): print(self.grid[j])
        print("----------")
        self.grid[y][x] = "-" 
        self.grid[y][x-1] = "A" 
        # segno lo spostamento nelle variabili
        self.agent_pos = y,x-1
        for j in range(3): print(self.grid[j])
        return "left"
    

