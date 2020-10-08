# Pyhton Libraries
import random
import numpy as np

# User defined libraries
from Agent import *
from Message import Message

class Defender(Agent):
    """Agent that will try to detect malicous traffic on the network and block it"""

    ### Static class variables

    # Network model size constants
    INPUT_SIZE = 1
    OUTPUT_SIZE = 1

    def __init__(self, epsilon= 1):
        super(Defender, self).__init__(epsilon= epsilon)

    def initializeModel(self):
        """Initializes the model of the agent, must set self.outputSize of model
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        model = Sequential()
        model.add(Dense(4, input_dim= Defender.INPUT_SIZE, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(Defender.OUTPUT_SIZE, activation='linear'))
        model.compile(loss= tf.keras.losses.Huber(), optimizer=Adam(lr=Agent.DEFAULT_LEARNING_RATE))
        self.model = model

    def inspect(self, message):
        """Returns the suspicion score on a range of 0 to 1 of the message
        Parameters
        ----------
            message
                message object containing message meta data

        Returns
        -------
            suspicionScore
                0 to 1 float value determining how suspicous the defender found the message

        """
        if random.random() < self.epsilon:
            return random.random()
        else:
            #return self.model.predict(message.asNetworkInputs())
            return random.random()

    def train(self):
        """Reviews the game memory and runs through one epoch of training for the model
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        minibatch = random.sample(self.memory, len(self.memory))
        self.lossHistory.losses_clear()
        for messageInputs, truth, in minibatch:     
            modelOutput = truth
            modelOutput = np.reshape(modelOutput, [1, Defender.OUTPUT_SIZE])
            self.model.fit(messageInputs, modelOutput, epochs= 1, verbose= 0, callbacks= [self.lossHistory])

        if self.epsilon > Agent.EPSILON_MIN: self.epsilon *= Agent.DEFAULT_EPSILON_DECAY

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
        self.score += reward
        self.memory.append([message.asNetworkInputs(), suspicionScore])

if __name__ == "__main__":
    epsilon = .5
    defender = Defender(epsilon= epsilon)
    print(defender.epsilon)
    print(defender.name)
    print(defender.score)
    print(defender.lossHistory)
    print(defender.lives)
    print(defender.model)

    args = ['','','', "127.0.0.0.1", '', '', '', '', '', '', '', '','','', Message.BENIGN_LABEL]
    message = Message(args)
    print(defender.addTrainingPoint(message, .5, 10))
    print(defender.score)
    print(defender.memory)
    print(defender.getLogsName())
    print(defender.getModelName())
    for i in range(5):
        print(defender.inspect(message))
    defender.saveModel()
    defender.loadModel()