from __future__ import division
from __future__ import print_function
from vizdoom import *
import numpy as np
import itertools as it
from time import time, sleep
import skimage.color, skimage.transform

# Creates and initializes ViZDoom environment
class DoomEnvironment():

    def __init__(self, config_file_path, show_window = False, mode = Mode.PLAYER, screen_format = ScreenFormat.GRAY8,
                 screen_resolution = ScreenResolution.RES_640X480):
        self.game = DoomGame()
        self.game.load_config(config_file_path)
        self.initialize_environment(show_window, mode, screen_format, screen_resolution)
        self.frame_repeat = 12

    def initialize_environment(self, show_window, mode, screen_format, screen_resolution):
        self.game.set_window_visible(show_window)
        self.game.set_mode(Mode.PLAYER)
        self.game.set_screen_format(screen_format)
        self.game.set_screen_resolution(screen_resolution)
        self.game.init()
        print("DOOM Game Initialized")

    def get_actions(self):
        n = self.game.get_available_buttons_size()
        actions = [list(a) for a in it.product([0, 1], repeat=n)]
        return actions

    def preprocess(self, image, resolution = (64, 64)):
        img = skimage.transform.resize(image, resolution)
        img = img.astype(np.float32)
        return img

    def run(self, agent, episodes_to_run = 100):
        return


    def watch(self, agent, episodes_to_watch = 10, frame_repeat = 12):
        self.game.set_window_visible(True)
        self.game.set_mode(Mode.ASYNC_PLAYER)
        self.game.init()

        actions = self.get_actions()

        for episode_num in range(episodes_to_watch):
            self.game.new_episode()

            while not self.game.is_episode_finished():
                
                state = preprocess(self.game.get_state().screen_buffer)
                state = state.reshape([1, 1, state.shape[0], state.shape[1]])
                best_action_index = agent.get_best_action(state)

                # Instead of make_action(a, frame_repeat) in order to make the animation smooth
                self.game.set_action(actions[best_action_index])
                for _ in range(frame_repeat):
                    self.game.advance_action()

            # Sleep between episodes
            sleep(1.0)
            score = self.game.get_total_reward()
            print("Episode Number:", episode_num,"Total score:", score)


