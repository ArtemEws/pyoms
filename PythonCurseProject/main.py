import torch
from Agent import Agent

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
file = input()
agent = Agent(device, file)
print(agent.test())
