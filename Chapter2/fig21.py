import numpy as np
import random
import matplotlib.pyplot as plt


def generate_bandit(mean, variance, k):
    bandits = []
    for _ in range(k):
        bandits.append(np.random.normal(loc = mean, scale = variance, size = 100))

    return bandits


def generate_rewards(bandits, variance): # generate reward function with mean is random selected in bandits
    rewards = []
    for bandit in bandits:
        mean = np.random.choice(bandit)
        rewards.append(np.random.normal(loc = mean, scale = variance, size = 1000))

    return rewards


if __name__ == "__main__":
    k = 10
    x_axis = list(range(1000))
    variance = 1
    true_value_mean = 1
    bandits = generate_bandit(true_value_mean, variance, k)
    rewards = generate_rewards(bandits, variance)
    plt.plot(x_axis, rewards[0])
    plt.show()
