# Python libraries
from collections import deque

import warnings
warnings.filterwarnings("ignore")

import os

import tensorflow as tf
from tensorflow.python import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import load_model
from keras import backend as K
import keras.losses

# User defined libraries
from LossHistory import LossHistory
from Message import Message

class Agent():
    """Abstract class to take care of all the interfacing with the game engine and model saving/loading, inherited by both players"""

    ### Static Class Variables
    MAX_DATA_LENGTH = 1000                                                                        # Max number of decision frames the Agent can remember from a fight, average is about 2000 per fight

    DEFAULT_MODELS_DIR_PATH = '../local_models'                                                          # Default path to the dir where the trained models are saved for later access
    DEFAULT_LOGS_DIR_PATH = '../local_logs'                                                              # Default path to the dir where training logs are saved for user review

    EPSILON_MIN = 0.1                                         # Minimum exploration rate for a trained model
    DEFAULT_EPSILON_DECAY = 0.999                             # How fast the exploration rate falls as training persists
    DEFAULT_DISCOUNT_RATE = 0.98                              # How much future rewards influence the current decision of the model
    DEFAULT_LEARNING_RATE = 0.0001

    ### Instance Functions
    def __init__(self, epsilon= 1):
        self.name = self.__class__.__name__
        self.epsilon = epsilon
        self.lossHistory = LossHistory()
        self.prepareForNextGame()
        if self.name != "Agent":
            self.initializeModel()

    def prepareForNextGame(self):
        """Wipes the game memory so it can be filled by the next game
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.lives = 10
        self.memory = deque(maxlen= Agent.MAX_DATA_LENGTH)

    def getModelName(self):
        """Returns the formatted model name for the current model"""
        return  self.name + "Model.m"

    def getLogsName(self):
        """Returns the formatted log name for the current model"""
        return self.name + "Logs.l"

    def saveModel(self):
        """Saves the currently trained model in the default naming convention ../models/{Class_Name}Model
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.model.save_weights(os.path.join(Agent.DEFAULT_MODELS_DIR_PATH, self.getModelName()))
        with open(os.path.join(Agent.DEFAULT_LOGS_DIR_PATH, self.getLogsName()), 'a+') as file:
            file.write(str(sum(self.lossHistory.losses) / len(self.lossHistory.losses)))
            file.write('\n')

    def loadModel(self):
        """Loads in pretrained model object ../models/{Class_Name}Model
        Parameters
        ----------
        None
        Returns
        -------
        None
        """
        self.model.load_weights(os.path.join(Agent.DEFAULT_MODELS_DIR_PATH, self.getModelName()))

    ### Abstract methods for the child Agent to implement
    def initializeModel(self):
        """Initializes the model of the agent, must set self.outputSize of model
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        raise NotImplementedError("Implement this is in the inherited agent")
    
    def train(self):
        """Reviews the game memory and runs through one epoch of training for the model
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        raise NotImplementedError("Implement this is in the inherited agent")

    def addTrainingPoint(self, message, suspicionScore, reward):
        """Adds one training point to the agents memory to review after the game
        
        Parameters
        ----------
            message
                 message object containing message meta data

            suspicionScore
                0 to 1 float value determining how suspicous the defender found the message

            reward
                the integer reward for the current state action sequence

        Returns
        -------
        None
        """
        raise NotImplementedError("Implement this is in the inherited agent")

if __name__ == "__init__":
    agent = Agent()
    print(agent.epsilon)
