import agent as ag;
import environment as e;

env = e.maze()
a = ag.agent(env)

for i in range(3):
    print(a.env.grid[i])

