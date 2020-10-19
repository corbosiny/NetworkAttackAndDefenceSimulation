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
    INPUT_SIZE = 20 * 3
    OUTPUT_SIZE = INPUT_SIZE + 1

    def __init__(self, datasetPath, epsilon= 1):
        """Constructor for Attacker agent
        Parameters
        ----------
        datasetPath
            String representing the file path to the dataset used for attack messages

        epsilon
            Float value representing the starting chance the agent makes random moves while training

        Returns
        -------
        None      
        """
        self.datasetPath = datasetPath
        self.loadDataset(datasetPath)
        super(Attacker, self).__init__(epsilon= epsilon) # Calling parent constructor

    def loadDataset(self, datasetPath):
        """loads in the dataset for generating background traffic
        Parameters
        ----------
        datasetPath
            String representing the file path to the dataset used for attack messages
        
        Returns
        -------
        None
        """
        self.dataset = pd.read_csv(datasetPath)

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

    def getAttack(self, trafficFlow, reachableNodes, infectionScores, infectedNodes, graph):
        """Initializes the model of the agent
        Parameters
        ----------
        trafficFlow
            The number of messages going to each node in the network this round
        
        reachable
            Binary array with 1 representing a node reachable by the infected network
        
        infectionScores
            Reward score for infecting each node in the network
        
        infectedNodes
            List of the IPs of the infected nodes in the graph

        graph
            networkx graph of the current state of the network

        Returns
        -------
        message
            message object containing meta data about the attack message
        """
        if random.random() < self.epsilon:
            origin = random.sample(graph.nodes(), 1)[0]
            return Message(['','','', origin, '', '', '', '', '', '', '', '','','', Message.MALICIOUS_LABEL])
            #reachableNodeIPs = [graph.nodes()[index] for enumerate(index, reachable) in reachableNodes if reachable]
            #destination = random.choice(reachableNodeIPs)
        else:
            #modelOutput = self.model.predict(attackerInputs)[0]
            #modelOutput = [reachable * score for reachable,score in list(zip(reachable, modelOutput))]
            #destinationIndex = np.argmax(modelOutput)
            #if destinationIndex == OUTPUT_SIZE - 1: return None
            #destination = graph.nodes()[destinationIndex]
            origin = random.sample(graph.nodes(), 1)[0]
            return Message(['','','', origin, '', '', '', '', '', '', '', '', '','','', Message.MALICIOUS_LABEL])
        #origin = self.findAttackPath(destination, infectedNodes, graph)
        #message = self.getRandomAttackMessage(origin, destination)
        #return message

    def findAttackPath(self, destination, infectedNodes, graph):
        """Finds the infected node that can attack the reachable node
        Parameters
        ----------
        destination
            IP of the desired node to attack

        infectedNodes
            List of the IPs of the infected nodes in the graph

        graph
            networkx graph of the current state of the network

        Returns
        -------
        origin
            IP of the infected node to launch the attack from
        """
        origin = None
        for node in infectedNodes:
           if graph.has_edge(node, destination):
               origin = node
               break
        return origin

    def getRandomAttackMessage(self, origin, destination):
        """Gets a random malicious message from the dataset
           Then reworks the origin and destination to fit the current network
        Parameters
        ----------
        origin
            IP of the infected node to launch the attack from

        destination
            IP of the desired node to attack

        Returns
        -------
        message
            Message object containing metadata of the attack message
        """
        index = random.randint(1, len(self.dataset.index))
        row = self.dataset.iloc[index]
        row[Message.ORIGIN_INDEX] = origin
        row[Message.DESTINATION_INDEX] = destination
        message = Message(row)
        return message

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
        for attackerInputs, reward, in minibatch:     
            modelOutput = reward
            #modelOutput = self.model.predict(attackerInpuits)[0]
            #for index, output in enumerate(modelOutput):
            #   if reachableNodes[index] == 0: modelOutput[index] = 0
            modelOutput = np.reshape(modelOutput, [1, Attacker.OUTPUT_SIZE])
            #self.model.fit(attackerInputs, modelOutput, epochs= 1, verbose= 0, callbacks= [self.lossHistory])

        if self.epsilon > Agent.EPSILON_MIN: self.epsilon *= Agent.DEFAULT_EPSILON_DECAY

    def addTrainingPoint(self, attackerInputs, reward):
        """Adds one training point to the agents memory to review after the game
        
        Parameters
        ----------
            attackerInputs
                 An array containing the set of reachable nodes and the reward for infecting each of those nodes

            reward
                the integer reward for the current state action sequence

        Returns
        -------
        None
        """
        self.score += reward
        self.memory.append([attackerInputs, reward])

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
    
