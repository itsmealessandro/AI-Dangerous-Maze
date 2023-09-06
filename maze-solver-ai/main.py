import agent as ag;
import environment as e;
import numpy as np

env = e.maze()
a = ag.agent(env)

a.train(10000, 100)

for i in range(3):
    print(a.en.grid[i])

rewards_per_thousand_episodes = np.split(np.array(a.rewards_all_episodes), 10000 / 1000)
count = 1000

print("******** Average reward per thousand episodes ********\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r / 1000)))
    count += 1000

print("*********** Q Table ***********")
for row in a.q_table:
    formatted_row = ["{:.2f}".format(value) for value in row]
    print(formatted_row)