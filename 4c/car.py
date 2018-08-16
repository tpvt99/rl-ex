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

epsilon = 1e-5

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


prob = generate_poisson_prob()
actions = list(range(-MAX_CARS_MOVE, MAX_CARS_MOVE+1))

"""
@ action positive for moving cars from pos 1 to pos 2
         negative for moving cars from pos 2 to pos 1

@ current_state the current states, list of 2 numbers [a,b] a is number of cars in pos1, b is number of cars in pos2
@ state_values the matrix containings all values of state. shape[0] is height, corresponding to number of cars in position 1
"""
def expected_value(current_state, state_values, action):
    returns = 0

    #next_temp_state = [max(0, min(MAX_CARS, current_state[0] - action)), max(0, min(MAX_CARS, current_state[1] + action))]
    #outs += (-2 * math.abs(action) + DISCOUNT * state_values[next_temp_state[0], next_temp_state[1]])

    for request1 in range(POISSON_UPPER_BOUND):
        for request2 in range(POISSON_UPPER_BOUND):

            rewards = 0
            
            prob_request_1 = prob["request"][1][request1]
            prob_request_2 = prob["request"][2][request2]

            max_car_request_1 = min(current_state[0], request1)
            max_car_request_2 = min(current_state[1], request2)
            
            next_cars_at_1 = current_state[0] - max_car_request_1
            next_cars_at_2 = current_state[1] - max_car_request_2

            rewards = (max_car_request_1 + max_car_request_2) * PRICE_CAR_RENTAL

            for return1 in range(POISSON_UPPER_BOUND):
                for return2 in range(POISSON_UPPER_BOUND):

                    prob_return_1 = prob["return"][1][return1]
                    prob_return_2 = prob["return"][2][return2]

                    max_car_return_1 = min(MAX_CARS - next_cars_at_1, return1)
                    max_car_return_2 = min(MAX_CARS - next_cars_at_2, return2)

                    next_cars_at_1 += max_car_return_1
                    next_cars_at_2 += max_car_return_2

                    total_prob = prob_request_1 * prob_request_2 * prob_return_1 * prob_return_2

                    if action >= 0:
                        car_moves = min(min(next_cars_at_1, action), MAX_CARS - next_cars_at_2)
                        next_cars_at_1 -= car_moves
                        next_cars_at_2 += car_moves
                    else:
                        car_moves = min(min(next_cars_at_2, abs(action)), MAX_CARS - next_cars_at_1)
                        next_cars_at_1 += car_moves
                        next_cars_at_2 -= car_moves

                    next_state = [next_cars_at_1, next_cars_at_2]
                    rewards -= abs(action) * PRICE_CAR_MOVE
                    returns += total_prob * (rewards + DISCOUNT * state_values[next_state[0], next_state[1]])

    return returns


def policy_evaluation(state_values, action):
    new_state_values = np.copy(state_values)
    while True:
        for i in state_values.shape[0]:
            for j in state_values.shape[1]:
                current_state = [i, j]
                rewards = expected_value(current_state, new_state_values, action)
                new_state_values[i][j] = rewards
        if abs(new_state_values - state_values) < epsilon:
            break

    return new_state_values


def policy_iterations():
    # step 1, initialization
    state_values = np.zeros((MAX_CARS, MAX_CARS))

    # step2 + step 2, policy evaluation and policy improvments
    while True:
        max_action = 0
        state_values = policy_evaluation(state_values, max_action)
        policy_stable = True
        for i in state_values.shape[0]:
            for j in state_values.shape[1]:
                action_val = list()
                current_state = [i, j]
                old_action = max_action
                for action in actions:
                    action_val.append(expected_value(current_state, state_values, action))
                max_action = action_val.index(max(action_val))
                if max_action != old_action:
                    policy_stable = False


        if policy_stable:
            return state_values, max_action






