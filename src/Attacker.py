# Pyhton Libraries
import random
import numpy as np
import pandas as pd
#import networkx # only uncommnet for testing

# User defined libraries
from Agent import *
from Message import Message

class Attacker(Agent):
    """Agent that will generate malicious traffic for the network and try not to be caught"""

    def __init__(self, datasetPath, networkSize, epsilon= 1):
        """Constructor for Attacker agent
        Parameters
        ----------
        datasetPath
            String representing the file path to the dataset used for attack messages

        networkSize
            Integer representing the number of devices in the network

        epsilon
            Float value representing the starting chance the agent makes random moves while training

        Returns
        -------
        None      
        """
        self.datasetPath = datasetPath
        self.loadDataset(datasetPath)
        self.INPUT_SIZE = networkSize * 3
        self.OUTPUT_SIZE = networkSize + 1
        self.TRAFFIC_FLOW_INDEX = 0
        self.REACHABLE_NODES_INDEX = int(self.INPUT_SIZE / 3)
        self.INFECTION_SCORES_INDEX = int((self.INPUT_SIZE / 3) * 2)
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
        """Initializes the model of the agent
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        model = Sequential()
        model.add(Dense(self.INPUT_SIZE, input_dim= self.INPUT_SIZE, activation='relu'))
        model.add(Dense(self.OUTPUT_SIZE * 2, activation='relu'))
        model.add(Dense(self.OUTPUT_SIZE, activation='linear'))
        model.compile(loss= tf.keras.losses.Huber(), optimizer=Adam(lr=Agent.DEFAULT_LEARNING_RATE))
        self.model = model

    def getAttack(self, trafficFlow, reachableNodes, infectionScores, infectedNodes, graph):
        """Initializes the model of the agent
        Parameters
        ----------
        trafficFlow
            The number of messages going to each node in the network this round
        
        reachableNodes
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
        
        index
            Index of the node being attacked in the graphs node list, is one greater than the lenght for a "by"
        """
        if random.random() < self.epsilon: 
            reachableNodeIndicies = [index for index, canReach  in enumerate(reachableNodes) if canReach] 
            reachableNodeIndicies += [self.OUTPUT_SIZE - 1]
            destinationIndex = random.choice(reachableNodeIndicies)
        else:
            attackerInputs = trafficFlow + reachableNodes + infectionScores
            formattedInputs = np.reshape(attackerInputs, [1, self.INPUT_SIZE])
            modelOutput = self.model.predict(formattedInputs)[0]
            validDestinations = [[index, score] for index, score in enumerate(modelOutput[:-1]) if reachableNodes[index]]
            validDestinations.append([len(modelOutput) - 1, modelOutput[-1]])
            destinationIndex = max(validDestinations, key=lambda x: x[1])[0]

        message = self.buildAttackMessage(destinationIndex, infectedNodes, graph)
        return message, destinationIndex

    def buildAttackMessage(self, destinationIndex, infectedNodes, graph):
        """Builds up the attack message for the desired node to infect
        Parameters
        ----------
        destinationIndex
            Integer index of the desired node to attack from the graph

        infectedNodes
            List of the IPs of the infected nodes in the graph

        graph
            networkx graph of the current state of the network

        Returns
        -------
        message
            The final attack message to return to the engine
        """
        if destinationIndex == self.OUTPUT_SIZE - 1: return None
        nodes = list(graph.nodes())
        destination = nodes[destinationIndex]
        origin = self.findAttackPath(destination, infectedNodes, graph)
        message = self.getRandomAttackMessage(origin, destination)
        return message

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
        for attackerInputs, indexChoice, reward, in minibatch:     
            formattedInputs = np.reshape(attackerInputs, [1, self.INPUT_SIZE])
            modelOutput = self.model.predict(formattedInputs)[0]
            modelOutput[indexChoice] = reward
            for index, output in enumerate(modelOutput[:-1]):
               if formattedInputs[0][self.REACHABLE_NODES_INDEX + index] == 0: modelOutput[index] = 0
            modelOutput = np.reshape(modelOutput, [1, self.OUTPUT_SIZE])
            self.model.fit(formattedInputs, modelOutput, epochs= 1, verbose= 0, callbacks= [self.lossHistory])

        if self.epsilon > Agent.EPSILON_MIN: self.epsilon *= Agent.DEFAULT_EPSILON_DECAY

    def addTrainingPoint(self, attackerInputs, attackIndex, reward):
        """Adds one training point to the agents memory to review after the game
        
        Parameters
        ----------
        attackerInputs
                An array containing the set of reachable nodes and the reward for infecting each of those nodes

        attackIndex
            The index in the list of nodes of the graph that were attacked this round

        reward
            the integer reward for the current state action sequence

        Returns
        -------
        None
        """
        self.score += reward
        self.memory.append([attackerInputs, attackIndex, reward])

if __name__ == "__main__":
    pass
    #Uncomment code below for testing
    # epsilon = 0
    # graph = networkx.DiGraph()
    # graphLen = 3
    # for i in range(graphLen):
    #     graph.add_node(i)
    # for i in range(graphLen):
    #     graph.add_edge(i, (i + 1) % graphLen)

    # attacker = Attacker("../datasets/defaultAttackDataset.csv", len(graph.nodes()), epsilon= epsilon)
    # trafficInfo = [2, 1, 3, 0, 1, 0, 0, 1, 0]
    # infectedNodes = [0]
    # attackIndex = 1
    # reward = 10

    # trafficFlow = trafficInfo[attacker.TRAFFIC_FLOW_INDEX : int(attacker.TRAFFIC_FLOW_INDEX+(attacker.INPUT_SIZE/3))]
    # reachable = trafficInfo[attacker.REACHABLE_NODES_INDEX : int(attacker.REACHABLE_NODES_INDEX+(attacker.INPUT_SIZE/3))]
    # infectionScores = trafficInfo[attacker.INFECTION_SCORES_INDEX : int(attacker.INFECTION_SCORES_INDEX+(attacker.INPUT_SIZE/3))]
    # print('Pre load: ')
    # attacker.getAttack(trafficFlow, reachable, infectionScores, infectedNodes, graph)
    # attacker.saveModel()
    # attacker.initializeModel()
    # print('Newly initialized model: ')
    # attacker.getAttack(trafficFlow, reachable, infectionScores, infectedNodes, graph)
    # attacker.loadModel()
    # print('Post loading: ')
    # attacker.getAttack(trafficFlow, reachable, infectionScores, infectedNodes, graph)
