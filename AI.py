import numpy
import time
import random
from cv2 import *
from PIL import ImageGrab
from collections import deque
import pickle
import os

import keras
from keras import *

from space_invaders import SpaceInvadersGame


image_cols = 160
image_rows = 200
stack_count = 4
# move left, move right, move left+shoot, move right+shoot, shoot, do nothing
action_count = 6

GAMMA = 0.99
OBSERVATION = 1000
EXPLORE = 100000
INITIAL_EPSILON = 0.1
FINAL_EPSILON = 0.0001
REPLAY_MEMORY = 50000
BATCH = 16
FRAME_PER_ACTION = 1


def save_obj(obj, name):
    with open('objects/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('objects/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def create_model():
    model = Sequential()
    model.add(keras.layers.Conv2D(32, (8, 8), strides=(4, 4), padding='same', input_shape=(image_rows, image_cols, stack_count)))
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


def play_frame(game, action, t, simplify=True):
    inputs = [0, 0, 0] # [move right, move left, fire bullet]
    # do nothing
    if action[0] == 1:
        pass
    # move right or move right + shoot
    elif int(action[1]) == 1 or int(action[3]) == 1:
        inputs[0] = 1
    # move left or move left + shoot
    elif int(action[2]) == 1 or int(action[4]) == 1:
        inputs[1] = 1
    # move left/right + shoot or shoot
    if int(action[3]) == 1 or int(action[4]) == 1 or int(action[5]) == 1:
        inputs[2] = 1

    print(inputs)
    name = "AI_at_time_" + str(t)
    reward, image, active = game.frame_step(simplify=simplify, inputs=inputs, name=name)
    image = prepare_image(image)
    return reward, image, active


def train_net(game, model, observe=False):
    D = load_obj("D")
#    D = deque()
    action = numpy.zeros(action_count)
    action[0] = 1

    t = load_obj("time")
    #    t = 0

    reward, image, active = play_frame(game=game, action=action, t=t, simplify=True)
    stacked_image = numpy.stack((image, image, image, image), axis=2)
    stacked_image = stacked_image.reshape(1, image_rows, image_cols, stack_count)

    if observe:
        OBSERVE = 9999999999
        epsilon = FINAL_EPSILON
        model.load_weights("models\model.h5")
        adam = keras.optimizers.Adam(1e-4)
        model.compile(loss='mse', optimizer=adam)
    else:
        OBSERVE = OBSERVATION
        epsilon = load_obj("epsilon")
#        epsilon = INITIAL_EPSILON
        model.load_weights("models\model.h5")

    while True:
        loss = 0
        Q_sa = 0
        action_index = 0
        reward = 0
        current_action = [False, False, False, False, False, False]

        if random.random() <= epsilon:
            action_index = random.randrange(action_count)
            current_action[action_index] = 1
        else:
            q = model.predict(stacked_image)
            max_Q = numpy.argmax(q)
            action_index = max_Q
            current_action[action_index] = 1

        if epsilon > FINAL_EPSILON and t > OBSERVE:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        reward, c_image, active = play_frame(game=game, action=current_action, t=t, simplify=True)
        last_time = time.time()
        c_image = c_image.reshape(1, c_image.shape[0], c_image.shape[1], 1)
        c_stacked_image = numpy.append(c_image, stacked_image[:, :, :, :3], axis=3)
        initial_stacked_image = c_stacked_image

        D.append((stacked_image, action_index, reward, c_stacked_image, active))
        if len(D) > REPLAY_MEMORY:
            D.popleft()

        if t > OBSERVE:
            train_batch(random.sample(D, BATCH), model, Q_sa, loss)
        if not active:
            stacked_image = initial_stacked_image
        else:
            stacked_image = c_stacked_image

        t += 1

        if t % 1000 == 0:
            model.save_weights("models\model.h5", overwrite=True)
            save_obj(D, "D")
            save_obj(t, "time")
            save_obj(epsilon, "epsilon")
            print("Objects Saved")


def train_batch(minibatch, model, Q_sa, loss):
    inputs = numpy.zeros((BATCH, image_rows, image_cols, stack_count), dtype=numpy.float32)
    targets = numpy.zeros((inputs.shape[0], action_count), dtype=numpy.float32)

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


def init_objs():
    D = deque()
    t = 0
    epsilon = INITIAL_EPSILON
    save_obj(D, "D")
    save_obj(t, "time")
    save_obj(epsilon, "epsilon")
    model = create_model()
    model.save_weights("models/model.h5", overwrite=True)


def prepare_image(image_data):
    image_data = convert_image(image_data)
    image_data = cv2.rotate(image_data, cv2.ROTATE_90_CLOCKWISE)
    image_data = cv2.flip(image_data, 1)
    imshow("AI's Screen", image_data)
    return image_data


def convert_image(image_data):
    new_image_data = cv2.resize(image_data, (200, 160))
    new_image_data = cv2.cvtColor(new_image_data, cv2.COLOR_BGR2GRAY)
    new_image_data = cv2.Canny(new_image_data, threshold1=100, threshold2=200)
    return new_image_data


def playGame(observe=False):
    game = SpaceInvadersGame()
    model = create_model()
    train_net(game=game, model=model, observe=observe)


#init_objs()
playGame(observe=False)
