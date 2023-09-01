import agent as ag;
import environment as e;

env = e.maze()
a = ag.agent(env)

a.train(1000,100)

for i in range(3):
    print(a.en.grid[i])

print("************************ Q Talbe ************************")

for row in a.q_table:
    formatted_row = ["{:.2f}".format(value) for value in row]
    print(formatted_row)

