import random
import numpy as np
from collections import deque
from collections import namedtuple
import torch


class ReplayMemory:

    def __init__(self, buffer_size, batch_size, seed, device):
        self.device = device
        self.action_size = 4
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "next_state", "reward", "done"])
        self.seed = random.seed(seed)

    def push(self, state, action, next_state, reward, done):
        e = self.experience(state, action, next_state, reward, done)
        self.memory.append(e)

    def sample(self):
        experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(self.device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(self.device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(
            self.device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(self.device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(
            self.device)

        return states, actions, next_states, rewards, dones

    def __len__(self):
        return len(self.memory)
