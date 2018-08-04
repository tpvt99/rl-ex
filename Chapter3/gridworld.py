import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table

WORLD_SPACE = 5
action_probs = {"U": 0.25, "D": 0.25, "R": 0.25, "L": 0.25}
discount = 0.9

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
        elif (i == 0 and j == 1):
            next_reward["D"] = 10
            next_position["D"] = [i+1, j]
        elif (i == 0 and j == 3):
            next_reward["D"] = 5
            next_position["D"] = [i+1, j]
        else:
            next_reward["D"] = 0
            next_position["D"] = [i+1, j]

        if j == 0:
            next_reward["L"] = -1
            next_position["L"] = [i, j]
        elif (i == 0 and j == 1):
            next_reward["L"] = 10
            next_position["L"] = [i, j-1]
        elif (i == 0 and j == 3):
            next_reward["L"] = 5
            next_position["L"] = [i, j-1]
        else:
            next_reward["L"] = 0
            next_position["L"] = [i, j-1]

        if j == WORLD_SPACE-1:
            next_reward["R"] = -1
            next_position["R"] = [i,j]
        elif (i == 0 and j == 1):
            next_reward["R"] = 10
            next_position["R"] = [i, j+1]
        elif (i == 0 and j == 3):
            next_reward["R"] = 5
            next_position["R"] = [i, j+1]
        else:
            next_reward["R"] = 0
            next_position["R"] = [i, j+1]

        temp_re.setdefault(j, next_reward)
        temp_pos.setdefault(j, next_position)

    positions.setdefault(i, temp_pos)
    rewards.setdefault(i, temp_re)

def draw_image(image):
    fig, ax = plt.subplots()
    ax.set_axis_off()
    tb = Table(ax, bbox[0,0,1,1])

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

print(positions)
print(rewards)
