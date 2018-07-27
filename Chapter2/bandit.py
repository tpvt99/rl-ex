import numpy as np
import random
import matplotlib.pyplot as plt
from operator import attrgetter

# we don't know the true value of the bandit. we need to choose which bandit to maximize the rewards received
class Bandit:
    def __init__(self, variance, size, stationary):
        self.values = np.random.normal(loc = 0, scale = variance, size = size)
        self.true_value = 0
        #self.rewards = np.random.normal(loc = self.true_value, scale = 1, size = size)
        self.stationary = stationary
        self.size = size

    def get_reward(self):
        return np.random.normal(loc = self.true_value, scale = 1, size = 1)

class KBanditProblem:

    def __init__(self, k_arms, variance, size, stationary, steps):
        self.k_arms = k_arms
        self.steps = steps
        self.variance = variance
        self.size = size
        self.stationary = stationary
        self.bandits = [Bandit(self.variance, self.size, self.stationary) for _ in range(self.k_arms)]
        self.reset()

    def reset(self):
        self.Q = np.zeros(self.k_arms)
        self.N = np.zeros(self.k_arms)
        self.average_reward = 0
        self.average_rewards = np.array([])
        self.optimal_percentage = 0
        self.optimal_percentages = np.array([])

    def get_optimal_action(self):
        return self.Q.argmax()

    def update_values_stationary(self, stationary):
        if not stationary:
            values = np.random.normal(loc = 0, scale = 0.01, size = self.k_arms)
            for i, bandit in zip(list(range(10)), self.bandits):
                bandit.true_value += values[i]


class KBanditSolution(KBanditProblem):

    def calculate_statistics(self, step, reward, action):
        self.average_reward += (1/step) * (reward - self.average_reward)
        self.average_rewards = np.append(self.average_rewards, self.average_reward)
        self.optimal_percentage += (1/step) * ((1 if action == self.bandits.index(max(self.bandits, key=attrgetter('true_value'))) else 0) - self.optimal_percentage)
        self.optimal_percentages = np.append(self.optimal_percentages, self.optimal_percentage)

    def solve_Egreedy(self, e):
        for k in range(self.steps):
            explore = random.uniform(0,1) < e
            if explore: # go to explore, else exploite
                action = np.random.choice(self.k_arms) # the number of the action
            else: # exploit
                action = self.get_optimal_action() # the number of the action
            
            self.update_values_stationary(stationary)
            reward = self.bandits[action].get_reward()
            self.N[action] += 1
            value = (1/self.N[action]) * (reward -self.Q[action])
            self.Q[action] += value
            self.calculate_statistics(k+1, reward, action)

if __name__ == "__main__":
    steps = 1000
    variance = 1
    k= 10 # 10-armed bandits
    size = 1000 # number of gaussian distribution
    stationary = 0

    # stationary
    bandit = KBanditSolution(k, variance, size, stationary, steps)
    bandit.solve_Egreedy(0)
    avgR1 = bandit.average_rewards
    optV1 = bandit.optimal_percentages
    print([bandit.true_value for bandit in bandit.bandits])
    print(bandit.Q)

    bandit.reset()
    bandit.solve_Egreedy(0.01)
    avgR2 = bandit.average_rewards
    optV2 = bandit.optimal_percentages
    print(bandit.Q)

    bandit.reset()
    bandit.solve_Egreedy(0.1)
    avgR3 = bandit.average_rewards
    optV3 = bandit.optimal_percentages
    print(bandit.Q)
    
    plt.figure(1)
    plt.plot(list(range(steps)), avgR1, 'r', list(range(steps)), avgR2, 'b', list(range(steps)), avgR3, 'g')

    plt.figure(2)
    plt.plot(list(range(steps)), optV1, 'r', list(range(steps)), optV2, 'b', list(range(steps)), optV3, 'g')

    plt.show()

