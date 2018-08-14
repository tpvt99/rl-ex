import numpy as np


MAX_CARS = 20

PRICE_CAR_RENTAL = 10

PRICE_CAR_MOVE = 2

MAX_CARS_MOVE = 5

DISCOUNT = 0.9

POISSON_UPPER_BOUND = 10

LAMBDA_REQUEST_1 = 3
LAMBDA_REQUEST_2 = 4

LAMBDA_RETURN_1 = 3
LAMBDA_RETURN_2 = 4 

def generate_poission_prob():
    out = dict()
    # request at pos 1
    pos = dict()
    pos[1] = [((LAMBDA_REQUEST_1**i) / (math.factorial(i)) * math.exp(-LAMBDA_REQUEST_1)) for i in range(POISSON_UPPER_BOUND)]
    # request at pos 2
    pos[2] = [((LAMBDA_REQUEST_2**i) / (math.factorial(i)) * math.exp(-LAMBDA_REQUEST_1)) for i in range(POISSON_UPPER_BOUND)]

    out["request"] = pos

    # return at pos 1
    pos = dict()
    pos[1] = [((LAMBDA_RETURN_1**i) / (math.factorial(i)) * math.exp(-LAMBDA_RETURN_1)) for i in range(POISSON_UPPER_BOUND)]
    # return at pos 2
    pos[2] = [((LAMBDA_RETURN_2**i) / (math.factorial(i)) * math.exp(-LAMBDA_RETURN_1)) for i in range(POISSON_UPPER_BOUND)]

    out["return"] = pos

    return out

"""
@ action positive for moving cars from pos 1 to pos 2
         negative for moving cars from pos 2 to pos 1

@ current_state the current states, list of 2 numbers [a,b] a is number of cars in pos1, b is number of cars in pos2
@ state_values the matrix containings all values of state. shape[0] is height, corresponding to number of cars in position 1
"""
def expected_value(current_state, state_values, action):
    out = 0

    next_temp_state = [max(0, min(MAX_CARS, current_state[0] - action)), max(0, min(MAX_CARS, current_state[1] + action))]
    outs += (-2 * math.abs(action) + DISCOUNT * state_values[next_temp_state[0], next_temp_state[1]]

    for pos1 in state_values.shape[0]:
        for pos2 in state_values.shape[1]:
            
        





