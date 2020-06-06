from replay_memory import ReplayMemory
from dqn import DQN
import torch.optim as optim
import torch.nn.functional as F
import torch
import numpy as np
import gym
import math
import random
from itertools import count

from gym.envs.classic_control import rendering
org_constructor = rendering.Viewer.__init__


def constructor(self, *args, **kwargs):
    org_constructor(self, *args, **kwargs)
    self.window.set_visible(visible=False)


rendering.Viewer.__init__ = constructor


class Agent():
    BATCH_SIZE = 64
    BUFFER_SIZE = 100000
    GAMMA = .99
    EPS_START = .9
    EPS_END = .05
    EPS_DECAY = .995
    LR = .0016
    STOP_FLAG = False
    device = 'cpu'
    policy_net = DQN().to(device)
    target_net = DQN().to(device)
    memory = ReplayMemory(buffer_size=BUFFER_SIZE,
                          batch_size=BATCH_SIZE, seed=0, device=device)
    optimizer = optim.Adam(policy_net.parameters(), lr=LR)
    gym.logger.set_level(40)
    env = gym.make('LunarLander-v2').unwrapped
    steps_done = 0
    score = 0

    def __init__(self, device, file=None):
        self.device = device
        if file:
            self.policy_net.load_state_dict(
                torch.load(file, map_location=device))

    def select_action(self, state, eps_threshold):
        sample = random.random()
        self.steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                self.policy_net.eval()
                result = self.policy_net(state)
                self.policy_net.train()
                return np.argmax(result.cpu().data.numpy())

        else:
            return torch.tensor([[random.randrange(4)]], device=self.device, dtype=torch.long)

    def test(self):
        test_rewards = []
        print('test')
        for i in range(100):
            state = self.env.reset()
            rewards = 0
            for j in count():
                self.condition.acquire()
                if self.STOP_FLAG:
                    break
                self.condition.release()
                action = self.select_action(torch.FloatTensor(state).to(self.device),
                                            eps_threshold=self.EPS_END + (self.EPS_START - self.EPS_END) * math.exp(
                                                -1. * i / self.EPS_DECAY))
                state, reward, done, _ = self.env.step(action.item())
                rewards += reward
                if done:
                    break
            self.score = rewards
            test_rewards.append(rewards)
            if self.STOP_FLAG:
                break
        self.env.close()
        return np.mean(test_rewards)

    def optimize_model(self):

        experiences = self.memory.sample()
        states, actions, next_states, rewards, dones = experiences

        Q_argmax = self.target_net(torch.tensor(
            next_states).to(self.device)).detach()
        _, a_prime = Q_argmax.max(1)

        Q_targets_next = self.target_net(torch.tensor(next_states).to(
            self.device)).detach().gather(1, a_prime.unsqueeze(1))

        Q_targets = torch.tensor(rewards).to(
            self.device) + (self.GAMMA * Q_targets_next * (1 - torch.tensor(dones).to(self.device)))

        Q_expected = self.policy_net(torch.tensor(states).to(self.device)).gather(
            1, torch.tensor(actions).to(self.device))

        loss = F.mse_loss(Q_targets, Q_expected)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def learn_model(self):
        just_rewards = [0]
        lr = self.LR
        all_rewards = []
        for i_episode in count():

            state = self.env.reset()

            rew_per_episode = 0
            for t in count():

                eps_threshold = self.EPS_END + \
                    (self.EPS_START - self.EPS_END) * \
                    math.exp(-1. * self.steps_done / self.EPS_DECAY)
                action = self.select_action(torch.FloatTensor(
                    state).to(self.device), eps_threshold)
                next_state, env_reward, done, _ = self.env.step(action.item())

                rew_per_episode += env_reward
                if (t > 400) & (action.item() != 0):
                    env_reward -= 0.3

                self.memory.push(state, action.item(),
                                 next_state, env_reward, done)

                state = next_state

                if len(self.memory) >= self.BATCH_SIZE:
                    self.optimize_model()
                if done:
                    all_rewards.append(rew_per_episode)
                    just_rewards.append(rew_per_episode)
                    break

                self.condition.acquire()
                if self.STOP_FLAG:
                    break
                self.condition.release()
                if t % 4 == 0:
                    self.target_net.load_state_dict(
                        self.policy_net.state_dict())
            print('\rEpisode {} \tLearning rate {:.6f} \tAverage Score: {:.2f}'.format(i_episode + 1, lr,
                                                                                       np.mean(just_rewards)), end="")
            self.score = np.mean(just_rewards)
            if (i_episode + 1) % 100 == 0:
                print('\rEpisode {} \tLearning rate {:.6f} \tAverage Score: {:.2f}'.format(i_episode + 1, lr,
                                                                                           np.mean(just_rewards)))
                just_rewards = []
                lr = self.LR / (i_episode + 1) * 100
                torch.save(self.policy_net.state_dict(), "model_mse_loss.nn")
                self.optimizer = optim.Adam(
                    self.policy_net.parameters(), lr=lr)
                if np.mean(just_rewards) >= 195:
                    test_count = 0
                    for test_i in range(3):
                        test_mark = self.test()
                        print(test_mark)
                        if test_mark >= 195:
                            test_count += 1
                    if test_count > 2:
                        break
            if self.STOP_FLAG:
                torch.save(self.policy_net.state_dict(), "model_mse_loss.nn")
                break
        self.env.close()
