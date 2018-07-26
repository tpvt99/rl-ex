import numpy as np
import random
import matplotlib.pyplot as plt
from operator import attrgetter

class Bandit:
    def __init__(self, variance, size, stationary):
        self.values = np.random.normal(loc = 0, scale = variance, size = size)
        self.rewards = np.random.normal(loc = np.random.choice(self.values), scale = 1, size = size)
        self.value = 0
        self.count = 0
        self.stationary = stationary
        self.size = size

    def get_reward(self):
        if not self.stationary:
            self.values += np.random.normal(loc = 0, scale = 0.01, size = self.size)
            return np.random.normal(loc = np.random.choice(self.values), scale = 1, size = 1)
        #return np.random.normal(loc = np.random.choice(self.values), scale = 1, size = 1)
        return np.random.choice(self.rewards)

    def update_count(self):
        self.count += 1
        return self.count

    def update_value(self, value):
        self.value += value


class KBanditSolution:

    def __init__(self, k_arms, variance, size, stationary, steps):
        self.k_arms = k_arms
        self.steps = steps
        self.variance = variance
        self.size = size
        self.stationary = stationary
        self.reset()

    def reset(self):
        self.bandits = [Bandit(self.variance, self.size, self.stationary) for _ in range(self.k_arms)]
        self.average_reward = 0
        self.average_rewards = np.array([])
        self.optimal_percentage = 0
        self.optimal_percentages = np.array([])


    def calculate_statistics(self, step, reward, action):
        self.average_reward += (1/step) * (reward - self.average_reward)
        self.average_rewards = np.append(self.average_rewards, self.average_reward)
        self.optimal_percentage += (1/step) * ((1 if action == max(self.bandits, key = attrgetter('value')) else 0) - self.optimal_percentage)
        self.optimal_percentages = np.append(self.optimal_percentages, self.optimal_percentage)


    def solve_Egreedy(self, e):
        for k in range(self.steps):
            explore = random.uniform(0,1) < e
            if explore: # go to explore, else exploite
                action = np.random.choice(self.bandits)
            else: # exploit
                action = max(self.bandits, key=attrgetter('value'))

            reward = action.get_reward()
            count = action.update_count()
            value = (1/count) * (reward - action.value)
            action.update_value(value)
            self.calculate_statistics(k+1, reward, action)

if __name__ == "__main__":
    steps = 1000
    variance = 1
    k= 10 # 10-armed bandits
    size = 1000 # number of gaussian distribution
    stationary = 1

    # stationary
    bandit = KBanditSolution(k, variance, size, stationary, steps)
    bandit.solve_Egreedy(0)
    avgR1 = bandit.average_rewards
    optV1 = bandit.optimal_percentages

    bandit.reset()
    bandit.solve_Egreedy(0.01)
    avgR2 = bandit.average_rewards
    optV2 = bandit.optimal_percentages

    bandit.reset()
    bandit.solve_Egreedy(0.1)
    avgR3 = bandit.average_rewards
    optV3 = bandit.optimal_percentages
    
    plt.figure(1)
    plt.plot(list(range(steps)), avgR1, 'r', list(range(steps)), avgR2, 'b', list(range(steps)), avgR3, 'g')

    plt.figure(2)
    plt.plot(list(range(steps)), optV1, 'r', list(range(steps)), optV2, 'b', list(range(steps)), optV3, 'g')

    plt.show()

