# Pyhton Libraries
import random
import numpy as np

# User defined libraries
from Agent import *
from Message import Message

class Attacker(Agent):
    """Agent that will generate malicious traffic for the network and try not to be caught"""

    ### Static class variables
    
    # Network model size constants
    INPUT_SIZE = 1
    OUTPUT_SIZE = 1

    def __init__(self, epsilon= 1):
        """Calls super constructor with the specificed epsilon value"""
        super(Attacker, self).__init__(epsilon= epsilon)

    def initializeModel(self):
        """Initializes the model of the agent, must set self.outputSize of model
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.model = None

    def getAttack(self, nodes):
        """Initializes the model of the agent
        Parameters
        ----------
        nodes
            List of all the node IPs in the network

        Returns
        -------
            message
                message object containing meta data about the attack message
        """
        if random.random() < self.epsilon:
            origin = random.sample(nodes, 1)[0]
            return Message(['','','', origin, '', '', '', '', '', '', '', '','','', Message.MALICIOUS_LABEL])
        else:
            origin = random.sample(nodes, 1)[0]
            return Message(['','','', origin, '', '', '', '', '', '', '', '','','', Message.MALICIOUS_LABEL])

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
            modelOutput = np.reshape(modelOutput, [1, Attacker.OUTPUT_SIZE])
            #self.model.fit(messageInputs, modelOutput, epochs= 1, verbose= 0, callbacks= [self.lossHistory])

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
    epsilon = 0
    attacker = Attacker(epsilon= epsilon)
    print(attacker.epsilon)
    print(attacker.name)
    print(attacker.score)
    print(attacker.lossHistory)
    print(attacker.lives)
    print(attacker.model)

    args = ['','','', "127.0.0.0.1", '', '', '', '', '', '', '', '','','', Message.BENIGN_LABEL]
    message = Message(args)
    print(attacker.addTrainingPoint(message, .5, 10))
    print(attacker.score)
    print(attacker.memory)
    print(attacker.getLogsName())
    print(attacker.getModelName())
    print(attacker.train())
    print(attacker.epsilon)
    
