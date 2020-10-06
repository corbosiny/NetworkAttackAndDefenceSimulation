# Pyhton Libraries
import random

# User defined libraries
from Agent import Agent

class Defender(Agent):
    """Agent that will try to detect malicous traffic on the network and block it"""

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
        pass

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
            return randon.random()
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
        for message, truth, reward in minibatch:     
            modelOutput = truth
            modelOutput = numpy.reshape(modelOutput, [1, self.outputSize])
            self.model.fit(message, modelOutput, epochs= 1, verbose= 0, callbacks= [self.lossHistory])

        if self.epsilon > Attacker.EPSILON_MIN: self.epsilon *= Attacker.DEFAULT_EPSILON_DECAY

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
        self.memory.append([message.asNetworkInputs(), suspicionScore])

if __name__ == "__main__":
    defender = Defender()
