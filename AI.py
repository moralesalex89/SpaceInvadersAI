import numpy
import time
import random
import cv2
from collections import deque

import keras
from keras import *

from space_invaders import SpaceInvadersGame
SpaceInvadersGame = SpaceInvadersGame()

image_cols = 40
image_rows = 20
stack_count = 4
# move left, move right, move left+shoot, move right+shoot, shoot, do nothing
action_count = 6

GAMMA = 0.99
OBSERVATION = 5000
EXPLORE = 100000
INITIAL_EPSILON = 0.1
FINAL_EPSILON = 0.0001
REPLAY_MEMORY = 50000
BATCH = 32
FRAME_PER_ACTION = 1


def convert_image(image_data):
    new_image_data = cv2.cvtColor(cv2.resize(image_data, (image_cols, image_rows)), cv2.COLOR_BGR2GRAY)
    ret, new_image_data = cv2.threshold(new_image_data, 1, 255, cv2.THRESH_BINARY)
    return new_image_data


def create_model():
    model = Sequential()
    model.add(keras.layers.Conv2D(32, (8, 8), strides=(4, 4), padding='same', input_shape=(image_cols, image_rows, stack_count)))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Conv2D(64, (4, 4), strides=(2, 2), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Conv2D(64, (3, 3), strides=(1, 1), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(512))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Dense(action_count))
    adam = keras.optimizers.Adam(1e-4)
    model.compile(loss='mse', optimizer=adam)
    return model


def play_frame(action, simplify=True):
    inputs = [False, False, False] # [move right, move left, fire bullet]
    # do nothing
    if action[0] == 1:
        pass
    # move right or move right + shoot
    elif action[1] or action[3]:
        inputs[0] = True
    # move left or move left + shoot
    elif action[2] or action[4]:
        inputs[1] = True
    # move left/right + shoot or shoot
    if action[3] or action[4] or action[5]:
        inputs[2] = True

    reward, image, active = SpaceInvadersGame.frame_step(simplify=simplify, inputs=inputs)
    converted_image = convert_image(image)

    return reward, converted_image, active


def train_net(model, active=True):
    D = deque()
    action = False ** action_count
    action[0] = True

    reward, image, active = play_frame(action=action, simplify=True)
    c_image = convert_image(image)
    c_image.reshape(1, 1, image_rows, image_cols)
    stacked_image = numpy.stack((c_image, c_image, c_image, c_image), axis=2)

    observe = OBSERVATION
    epsilon = INITIAL_EPSILON
    t = 0

    while True:
        loss = 0
        Q_sa = 0
        action_index = 0
        reward = 0
        current_action = False ** action_count

        if random.random() <= epsilon:
            action_index = random.randrange(action_count)
            current_action[action_index] = 1
        else:
            q = model.predict(stacked_image)
            max_Q = numpy.argmax(q)
            action_index = max_Q
            current_action[action_index] = 1

        if epsilon > FINAL_EPSILON and t > observe:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        reward, c_image, active = play_frame(action=action, simplify=True)
        last_time = time.time()
        c_image = c_image.reshape(1, c_image.shape[0], c_image.shape[1], 1)
        c_stacked_image = numpy.append(c_image, stacked_image[:, :, :, :3], axis=3)

        D.append((stacked_image, action_index, reward, c_stacked_image, active))
        if len(D) > REPLAY_MEMORY:
            D.popleft()

        if t > observe:
            train_batch(random.sample(D, BATCH), model, Q_sa, loss)
        stacked_image = c_stacked_image
        t += 1


def train_batch(minibatch, model, Q_sa, loss):
    inputs = numpy.zeros((BATCH, image_rows, image_cols, stack_count), dtype=bool)
    targets = numpy.zeros((inputs.shape[0], action_count))

    for i in range(0, len(minibatch)):
        curr_state = minibatch[i][0]
        curr_action = minibatch[i][1]
        curr_reward = minibatch[i][2]
        next_state = minibatch[i][3]
        active = minibatch[i][4]
        inputs[i:i + 1] = curr_state
        targets[i] = model.predict(curr_state)
        Q_sa = model.predict(next_state)
        if active:
            targets[i, curr_action] = curr_reward
        else:
            targets[i, curr_action] = curr_reward + GAMMA * numpy.max(Q_sa)

    loss += model.train_on_batch(inputs, targets)


def playGame(observe=False):
    game = SpaceInvadersGame()
    model = create_model()
    train_net(model)


playGame()
