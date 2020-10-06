# Pyhton Libraries
import random

# User defined libraries
from Agent import Agent

class Attacker(Agent):
    """Agent that will generate malicious traffic for the network and try not to be caught"""

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
        pass

    def getAttack(self):
        """Initializes the model of the agent
        Parameters
        ----------
        TBD

        Returns
        -------
            message
                message object containing meta data about the attack message
        """
        if self.epsilon < Attacker.EPSILON_MIN:
            pass
        else:
            pass

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
        for state, action, reward in minibatch:     
            modelOutput = self.model.predict(state)[0]

            modelOutput[action] = reward

            modelOutput = numpy.reshape(modelOutput, [1, self.outputSize])
            self.model.fit(state, modelOutput, epochs= 1, verbose= 0, callbacks= [self.lossHistory])

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
        pass

if __name__ == "__main__":
    attacker = Attacker(epsilon= args.epsilon)
