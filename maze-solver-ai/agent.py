import random;
import numpy as np
import environment as env

class agent:

    en = env.maze()
    
    def __init__(self,environment):
        self.en = environment
    
    def go_up(self):
        return self.en.agent_move("up")
    
    def go_down(self):
        return self.en.agent_move("down")
    
    def go_right(self):
        return self.en.agent_move("right")
    
    def go_left(self):
        return self.en.agent_move("left")
    
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
    exploration_decay_rate = 0.01

    # valore che influienza il peso delle nuove informazioni rispetto a quelle passate
    learning_rate = 0.1

    # valore che influenza il peso dei futuri rewards rispetto a quelli immediati
    discount_rate = 0.99

    # Tabella che tiene traccia delle ricompense ottenute per ogni possibile azione ad ogni possibile stato
    q_table = np.zeros((30, 4))  # 30 stati e 4 azioni possibili per ogni stato, quindi una matrice 30x2

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
                print("-------------------- step %d:--------------------" % step)
                action_index = None
                # explore - exploit tradeoff
                if self.exploration_rate < random.uniform(0, 1):
                    # sceglie l'azione con qualità maggiore
                    
                    action_index = np.argmax(self.q_table[self.state,:])
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
                    new_state = self.state -10 # la posizione [0][0] è lo stato 0, la [0][1] è lo stato 1, la [1][0] è lo stato 10
                elif result == "down":
                    reward = 0
                    new_state = self.state +10
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
                    new_state = 9
                    reward = 0.5
                else:
                    raise Exception("result ha un valore sbagliato")

                
                

                # Aggiorno la Q table 
                self.q_table[self.state, action_index] = self.q_table[self.state, action_index] * (1 - self.learning_rate) + \
                self.learning_rate * (reward + self.discount_rate * np.max(self.q_table[new_state, :]))

                print("reward: %g" % reward  )
                print("value: %g" % self.q_table[self.state][action_index])

                # Setto il nuovo stato
                self.state = new_state

                # stampa passo
                print("nuova pos agente %d,%d" %(self.en.agent_pos[0],self.en.agent_pos[1]))
                print("state: %d" % self.state)
                

                

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

            print("CountQ: %d , CountR: %d" %(count_Q,count_R) )