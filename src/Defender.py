# Pyhton Libraries
import random
import numpy as np

# User defined libraries
from Agent import *
from Message import Message

class Defender(Agent):
    """Agent that will try to detect malicous traffic on the network and block it"""

    ### Static class variables
    DEFAULT_LEARNING_RATE = .001

    # Network model size constants
    INPUT_SIZE = 4
    OUTPUT_SIZE = 4

    # Membership function for suspicion scores
    NO_SUSPICION_LABEL = 'NONE'
    LOW_SUSPICION_LABEL = 'LOW'
    MEDIUM_SUSPICION_LABEL = 'MEDIUM'
    HIGH_SUSPICION_LABEL = 'HIGH'

    SUSPICION_LABELS = [NO_SUSPICION_LABEL, LOW_SUSPICION_LABEL, MEDIUM_SUSPICION_LABEL, HIGH_SUSPICION_LABEL]

    def __init__(self, epsilon= 1):
        super(Defender, self).__init__(epsilon= epsilon)

    def initializeModel(self):
        """Initializes the model of the agent
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        model = Sequential()
        model.add(Dense(8, input_dim= Defender.INPUT_SIZE, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(Defender.OUTPUT_SIZE, activation='linear'))
        model.compile(loss= tf.keras.losses.Huber(), optimizer=Adam(lr=Agent.DEFAULT_LEARNING_RATE))
        self.model = model

    def inspect(self, message):
        """Returns the suspicion score on a range of 0 to 1 of the message
        Parameters
        ----------
        message
            message object containing message metadata

        Returns
        -------
        suspicionLabel
            String membership label representing the suspicion range the message belongs in

        """
        if random.random() < self.epsilon:
            return random.sample(Defender.SUSPICION_LABELS, 1)[0]
        else:
            formattedInputs =  np.reshape(message.asNetworkInputs(), [1, Defender.INPUT_SIZE])
            modelOutput = self.model.predict(formattedInputs)[0]
            index = np.argmax(modelOutput)
            return Defender.SUSPICION_LABELS[index]

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
        for messageInputs, label, reward in minibatch:
            formattedInputs = np.reshape(messageInputs, [1, Defender.INPUT_SIZE])  
            modelOutput = self.model.predict(formattedInputs)[0]
            modelOutput[Defender.SUSPICION_LABELS.index(label)] = reward
            modelOutput = np.reshape(modelOutput, [1, Defender.OUTPUT_SIZE])
            self.model.fit(formattedInputs, modelOutput, epochs= 1, verbose= 0, callbacks= [self.lossHistory])

        if self.epsilon > Agent.EPSILON_MIN: self.epsilon *= Agent.DEFAULT_EPSILON_DECAY

    def addTrainingPoint(self, message, suspicionLabel, reward):
        """Adds one training point to the agents memory to review after the game
        
        Parameters
        ----------
        message
                message object containing message meta data

        suspicionLabel
            String membership label for the suspicion range this message was flagged for

        reward
            the integer reward for the current state action sequence

        Returns
        -------
        None
        """
        self.score += reward
        self.memory.append([message.asNetworkInputs(), suspicionLabel, reward])

if __name__ == "__main__":
    epsilon = 0
    defender = Defender(epsilon= epsilon)
    defender.saveModel()
    #print(defender.epsilon)
    #print(defender.name)
    #print(defender.score)
    #print(defender.lossHistory)
    #print(defender.model)


