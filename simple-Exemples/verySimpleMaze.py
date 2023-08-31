import numpy as np
import random


class environment:
    maze = []

    agent_pos = 0

    def __init__(self):
        self.maze = ["A", 0, 0, "T"]

    def reset(self):
        self.maze = ["A", 0, 0, "T"]
        self.agent_pos = 0

    # Agent movement right
    def right(self):
        print("l: %d" % self.agent_pos)
        # se l'agente va fuori mappa
        if self.agent_pos + 1 > 3:
            return "out"
        # se l'agente raggiunge il target
        if self.maze[self.agent_pos + 1] == "T":
            return "r-win"
        # l'agente  si sposta
        self.maze[self.agent_pos] = 0
        self.maze[self.agent_pos + 1] = "A"
        self.agent_pos += 1
        return "right"

        # Agent movement left

    def left(self):
        print("l: %d" % self.agent_pos)
        # se l'agente va fuori mappa
        if self.agent_pos - 1 < 0:
            return "out"
        # se l'agente raggiunge il target
        if self.maze[self.agent_pos - 1] == "T":
            return "l-win"
        # l'agente si sposta
        self.maze[self.agent_pos] = 0
        self.maze[self.agent_pos - 1] = "A"
        self.agent_pos -= 1
        return "left"


class agent:

    
    env = None

    def __init__(self, maze):
        self.env = maze

    # Agent Movements

    def right(self):
        return self.env.right()

    def left(self):
        return self.env.left()

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
    q_table = np.zeros((4, 2))  # 4 stati e 2 azioni possibili per ogni stato, quindi una matrice 4x2

    # valore che definisce in che stato si trova l'agente
    state = 0

    # IA Main function
    def train(self, num_ep, max_steps):
        self.episodes_num = num_ep
        self.steps_max = max_steps

        # ************************************ Inizio algoritmo di Q learing ************************************ 
        for episode in range(num_ep):
            # resetto la posizione dell'agente e la mappa
            self.env.reset()
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
                print("---- step %d:----" % step)
                action_index = None
                # explore - exploit tradeoff
                if self.exploration_rate < random.uniform(0, 1):
                    # sceglie l'azione con qualità maggiore

                    action_val = max(self.q_table[self.state, :])
                    count_Q += 1
                else:
                    action_index = random.randint(0, 1)
                    # sceglie un'azione casuale
                    action_val = self.q_table[self.state][action_index]
                    count_R += 1

                # cerco l'azione corrispondete al valore
                if action_index is not None:
                    if action_index == 0:
                        result = self.right()
                    else:
                        result = self.left()
                else:
                    if self.q_table[self.state][0] == action_val:
                        result = self.right()
                        action_index = 0
                    else:
                        result = self.left()
                        action_index = 1

                reward = None
                new_state = None
                # analisi del reward
                if result == "right":
                    reward = 0
                    new_state = self.state + 1
                elif result == "left":
                    reward = 0
                    new_state = self.state - 1
                elif result == "out":
                    reward = -1
                    new_state = self.state
                elif result == "l-win":
                    reward = 1
                    new_state = self.state
                    done = True
                elif result == "r-win":
                    reward = 1
                    new_state = self.state
                    done = True
                result = None

                # Update Q-table for Q(s,a)

                self.q_table[self.state][action_index] = self.q_table[self.state][action_index] * (1 - self.learning_rate) +\
                self.learning_rate * (reward + self.discount_rate * max(self.q_table[new_state, :]))

                print("reward: %g" % reward  )
                print("value: %g" % self.q_table[self.state][action_index])

                # Setto il nuovo stato
                self.state = new_state

                # stampa passo
                print(self.env.agent_pos)
                print("state: %d" % self.state)
                print(self.env.maze)

                # TODO episode reward

                # controllo se abbiamo terminato l'episodio
                rewards_current_episode += reward 
                if done == True:
                    print("Vittoria")
                    break

            # Exploration rate decay
            self.exploration_rate = self.min_exploration_rate + \
                                    (self.max_exploration_rate - self.min_exploration_rate) * np.exp(
                -self.exploration_decay_rate * episode)
            # Add current episode reward to total rewards list
            self.rewards_all_episodes.append(rewards_current_episode)

            print("CountQ: %d , CountR: %d" %(count_Q,count_R) )
            


# Main
en = environment()
ag = agent(en)
ag.train(10000, 20)

# Calculate and print the average reward per thousand episodes
rewards_per_thousand_episodes = np.split(np.array(ag.rewards_all_episodes),10000/1000)
count = 1000

print("********Average reward per hundred episodes********\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000

print("*********** Q Table ***********")
print(ag.q_table)