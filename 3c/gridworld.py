import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table

WORLD_SPACE = 5
action_probs = {"U": 0.25, "D": 0.25, "R": 0.25, "L": 0.25}
DISCOUNT = 0.9
A_POS = [0, 1]
B_POS = [0, 3]
A_PRIME_POS = [4, 1]
B_PRIME_POS = [2, 3]

positions = {}
rewards = {}

for i in range(WORLD_SPACE):
    temp_re = dict()
    temp_pos = dict()
    for j in range(WORLD_SPACE):
        next_reward = {}
        next_position = {}

        if i == 0:
            next_reward["U"] = -1
            next_position["U"] = [i, j]
        else:
            next_reward["U"] = 0
            next_position["U"] = [i-1, j]

        if i == WORLD_SPACE - 1:
            next_reward["D"] = -1
            next_position["D"] = [i, j]
        else:
            next_reward["D"] = 0
            next_position["D"] = [i+1, j]

        if j == 0:
            next_reward["L"] = -1
            next_position["L"] = [i, j]
        else:
            next_reward["L"] = 0
            next_position["L"] = [i, j-1]

        if j == WORLD_SPACE-1:
            next_reward["R"] = -1
            next_position["R"] = [i,j]
        else:
            next_reward["R"] = 0
            next_position["R"] = [i, j+1]

        if [i, j] == A_POS:
            next_reward["R"] = next_reward["L"] = next_reward["D"] = next_reward["U"] = 10
            next_position["R"] = next_position["L"] = next_position["D"] = next_position["U"] = A_PRIME_POS

        if [i,j] == B_POS:
            next_reward["R"] = next_reward["L"] = next_reward["D"] = next_reward["U"] = 5
            next_position["R"] = next_position["L"] = next_position["D"] = next_position["U"] = B_PRIME_POS


        temp_re.setdefault(j, next_reward)
        temp_pos.setdefault(j, next_position)

    positions.setdefault(i, temp_pos)
    rewards.setdefault(i, temp_re)

def draw_image(image):
    fig, ax = plt.subplots()
    ax.set_axis_off()
    tb = Table(ax, bbox = [0,0,1,1])

    nrows, ncols = image.shape
    width, height = 1.0 /ncols, 1.0/nrows

    for (i,j), val in np.ndenumerate(image):
        idx = [j% 2, (j+1) % 2] [i % 2]
        color ='white'

        tb.add_cell(i,j,width,height,text=val,loc="center",facecolor=color)

    # Row Labels...
    for i, label in enumerate(range(len(image))):
        tb.add_cell(i, -1, width, height, text=label+1, loc='right',
                    edgecolor='none', facecolor='none')
    # Column Labels...
    for j, label in enumerate(range(len(image))):
        tb.add_cell(-1, j, width, height/2, text=label+1, loc='center',
                           edgecolor='none', facecolor='none')
    ax.add_table(tb)
    plt.show()

def update_state_value():
    state_values = np.zeros((WORLD_SPACE, WORLD_SPACE))
    new_state_values = np.copy(state_values)
    while True:
        for i in range(WORLD_SPACE):
            for j in range(WORLD_SPACE):
                reward = 0
                for action in action_probs.keys():
                    new_position = positions[i][j][action]
                    reward += action_probs[action] * (rewards[i][j][action] + DISCOUNT * state_values[new_position[0], new_position[1]])
                new_state_values[i][j] = reward

        if np.sum(abs(new_state_values - state_values)) < 1e-4:
            draw_image(np.round(new_state_values, decimals = 1))
            break
        state_values = np.copy(new_state_values)

if __name__ == "__main__":
    update_state_value()
