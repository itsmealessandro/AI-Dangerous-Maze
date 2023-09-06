import numpy as np
import random


class maze:
    grid = []

    # uso una coppia per rappresentare la posizione dell'agente nell'ambiente
    agent_pos = 0, 0

    def __init__(self):
        self.grid = [
            ["A", 0, 0],
            [0, "H", "O"],
            ["P", 0, "T"]
        ]

    def reset(self):
        self.grid = [
            ["A", 0, 0],
            [0, "H", "O"],
            ["P", 0, "T"]
        ]
        self.agent_pos = 0, 0

    # ******************** Agent Movements ********************
    def A_move_up(self):
        y = self.agent_pos[0]
        x = self.agent_pos[1]
        print("up, posizione agente: %d %d" % (y, x))
        if y - 1 < 0:
            return "out"
        elif self.grid[y - 1][x] == "H":
            return "hole"
        elif self.grid[y - 1][x] == "T":
            return "win"
        elif self.grid[y - 1][x] == "P":
            self.grid[y][x] = 0
            self.grid[1][2] = "A"
            self.agent_pos = 1, 2
            return "portal"
        # sposto l'agente visivamente
        for j in range(3): print(self.grid[j])
        print("----------")
        self.grid[y][x] = 0
        self.grid[y - 1][x] = "A"
        # segno lo spostamento nelle variabili
        self.agent_pos = y - 1, x
        for j in range(3): print(self.grid[j])
        return "up"

    def A_move_down(self):

        y = self.agent_pos[0]
        x = self.agent_pos[1]
        print("down, posizione agente: %d %d" % (y, x))
        if y + 1 > 2:
            return "out"
        elif self.grid[y + 1][x] == "H":
            return "hole"
        elif self.grid[y + 1][x] == "T":
            return "win"
        elif self.grid[y + 1][x] == "P":
            self.grid[y][x] = 0
            self.grid[1][2] = "A"
            self.agent_pos = 1, 2
            return "portal"
        # sposto l'agente visivamente
        for j in range(3): print(self.grid[j])
        print("----------")
        self.grid[y][x] = 0
        self.grid[y + 1][x] = "A"
        # segno lo spostamento nelle variabili
        self.agent_pos = y + 1, x
        for j in range(3): print(self.grid[j])
        return "down"

    def A_move_right(self):
        y = self.agent_pos[0]
        x = self.agent_pos[1]
        print("right, posizione agente: %d %d" % (y, x))
        if x + 1 > 2:
            return "out"
        elif self.grid[y][x + 1] == "H":
            return "hole"
        elif self.grid[y][x + 1] == "T":
            return "win"
        elif self.grid[y][x + 1] == "P":
            self.grid[y][x] = 0
            self.grid[1][2] = "A"
            self.agent_pos = 1, 2
            return "portal"
        # sposto l'agente visivamente
        for j in range(3): print(self.grid[j])
        print("----------")
        self.grid[y][x] = 0
        self.grid[y][x + 1] = "A"
        # segno lo spostamento nelle variabili
        self.agent_pos = y, x + 1
        for j in range(3): print(self.grid[j])
        return "right"

    def A_move_left(self):
        y = self.agent_pos[0]
        x = self.agent_pos[1]
        print("left, posizione agente: %d %d" % (y, x))
        if x - 1 < 0:
            return "out"
        elif self.grid[y][x - 1] == "H":
            return "hole"
        elif self.grid[y][x - 1] == "T":
            return "win"
        elif self.grid[y][x - 1] == "P":
            self.grid[y][x] = 0
            self.grid[1][2] = "A"
            self.agent_pos = 1, 2
            return "portal"
        # sposto l'agente visivamente
        for j in range(3): print(self.grid[j])
        print("----------")
        self.grid[y][x] = 0
        self.grid[y][x - 1] = "A"
        # segno lo spostamento nelle variabili
        self.agent_pos = y, x - 1
        for j in range(3): print(self.grid[j])
        return "left"


class agent:
    state = 0
    en = maze()

    def __init__(self, env):
        self.en = env

    def go_up(self):
        return self.en.A_move_up()

    def go_down(self):
        return self.en.A_move_down()

    def go_right(self):
        return self.en.A_move_right()

    def go_left(self):
        return self.en.A_move_left()

    # episodes and steps 
    episodes_num = 0
    steps_max = 0

    rewards_all_episodes = []

    # ************************************************ Q learing variables ************************************************
    # valore con che influenza l'agente a esplorare la mappa piuttosto che a fare scelte dettate da ciò che ha imparato
    exploration_rate = 1
    min_exploration_rate = 0.01
    max_exploration_rate = 1
    # valore che disincentiva l'agente a esplorare la mappa
    exploration_decay_rate = 0.02

    # valore che influienza il peso delle nuove informazioni rispetto a quelle passate
    learning_rate = 0.1

    # valore che influenza il peso dei futuri rewards rispetto a quelli immediati
    discount_rate = 0.99

    # Tabella che tiene traccia delle ricompense ottenute per ogni possibile azione ad ogni possibile stato
    q_table = np.zeros((9, 4))  # 9 stati e 4 azioni possibili per ogni stato, quindi una matrice 9x2

    # valore che definisce in che stato si trova l'agente
    state = 0

    # IA Main function
    def train(self, num_ep, max_steps):
        self.episodes_num = num_ep
        self.steps_max = max_steps

        # ************************************ Inizio algoritmo di Q learing ************************************ 
        for episode in range(num_ep):
            # resetto la posizione dell'agente e la mappa
            self.en.reset()
            self.state = 0
            # varaibile per sapere se è terminato l'episodio prima dei massimi step
            done = False

            rewards_current_episode = 0

            count_Q = 0
            count_R = 0

            # stampa episodio
            print("************************************ Episode %d ************************************" % episode)

            # ciclo che determina le azioni dell'agente
            for step in range(max_steps):
                print("---------- step %d:----------" % step)
                action_index = None
                # explore - exploit tradeoff
                if self.exploration_rate < random.uniform(0, 1):
                    # sceglie l'azione con qualità maggiore

                    action_index = np.argmax(self.q_table[self.state, :])
                    count_Q += 1
                else:
                    # sceglie un'azione casuale
                    action_index = random.randint(0, 3)

                    count_R += 1

                # cerco l'azione corrispondete al valore
                if action_index == 0:
                    result = self.go_up()
                elif action_index == 1:
                    result = self.go_down()
                elif action_index == 2:
                    result = self.go_right()
                else:
                    result = self.go_left()

                reward = None
                new_state = None
                # analisi del reward

                if result == "up":
                    reward = 0
                    new_state = self.state - 3  # la posizione [0][0] è lo stato 0, la [0][1] è lo stato 1, la [1][0] è lo stato 3
                elif result == "down":
                    reward = 0
                    new_state = self.state + 3
                elif result == "right":
                    reward = 0
                    new_state = self.state + 1
                elif result == "left":
                    reward = 0
                    new_state = self.state - 1
                elif result == "out":
                    reward = -1
                    new_state = self.state
                elif result == "win":
                    reward = 1
                    new_state = self.state
                    done = True
                elif result == "hole":
                    new_state = self.state
                    reward = -1
                    done = True
                elif result == "portal":
                    new_state = 5
                    reward = 0

                # Update Q-table for Q(s,a)
                print(self.state)
                print(action_index)
                self.q_table[self.state, action_index] = self.q_table[self.state, action_index] * (
                        1 - self.learning_rate) + \
                                                         self.learning_rate * (reward + self.discount_rate * np.max(
                    self.q_table[new_state, :]))

                print("reward: %g" % reward)
                print("value: %g" % self.q_table[self.state][action_index])

                # Setto il nuovo stato
                self.state = new_state

                # stampa passo
                print("nuova pos agente %d,%d" % (self.en.agent_pos[0], self.en.agent_pos[1]))
                print("state: %d" % self.state)
                for j in range(3):
                    print(self.en.grid[j])

                # controllo se abbiamo terminato l'episodio + episode reward
                rewards_current_episode += reward
                if done == True and result == "win":
                    print("Vittoria")
                    result = None
                    break
                elif done == True and result == "hole":
                    print("Sconfitta")
                    result = None
                    break

                # resetto result
                result = None

            # Exploration rate decay
            self.exploration_rate = self.min_exploration_rate + \
                                    (self.max_exploration_rate - self.min_exploration_rate) * np.exp(
                -self.exploration_decay_rate * episode)
            # Add current episode reward to total rewards list
            self.rewards_all_episodes.append(rewards_current_episode)

            print("CountQ: %d , CountR: %d" % (count_Q, count_R))


# Main

env = maze()
ag = agent(env)

ag.train(10000, 50)

# Calculate and print the average reward per thousand episodes
rewards_per_thousand_episodes = np.split(np.array(ag.rewards_all_episodes), 10000 / 1000)
count = 1000

print("******** Average reward per thousand episodes ********\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r / 1000)))
    count += 1000

print("*********** Q Table ***********")
for row in ag.q_table:
    formatted_row = ["{:.2f}".format(value) for value in row]
    print(formatted_row)

# print(ag.q_table.)
