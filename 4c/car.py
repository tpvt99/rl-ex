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

@ current_state the current states
@ state_values the matrix containings all values of state
"""
def expected_value(current_state, state_values, action):
    





