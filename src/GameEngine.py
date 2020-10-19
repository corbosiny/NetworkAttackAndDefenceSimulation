# Pyhton Libraries
import argparse
import networkx
import random
import pandas as pd
import matplotlib.pyplot as plt
import time
import math

# User defined libraries
from Attacker import Attacker
from Defender import Defender
from Message import Message

class GameEngine():
    """
        Class responsible for running the attacker/defender simulation of an IOT network.

        A network structure is provided via a text file to act as the battleground. The attacker
        is tasked with trying to mask it's activity on the network in order to successfully execute
        phishing attacks. While the defender is trying to detect this malicious behavior and reject
        those infected communications. Each side is given a number of lives, upon being breached the
        defender loses one life. Upon being detected the attacker loses one life. The game is played
        until one of the two run out of lives. The thought process of the attacker in terms of how
        suspicous a node is in the network is updated during play. Random background traffic of the
        network is also simulated for the attacker to slip inbetween to avoid detection.

        Reinforcement learning is utilized at the end of every game using Q learning to improve both
        combatants in their roles.
    """

    ### Static Class Variables

    MAX_BACKGROUND_TRAFFIC_MESSAGES = 20                      # The maximum number of background messages between attacks

    COLOR_MAP = {Defender.NO_SUSPICION_LABEL  : 'blue', Defender.LOW_SUSPICION_LABEL  : 'yellow', Defender.MEDIUM_SUSPICION_LABEL :  'orange', Defender.HIGH_SUSPICION_LABEL : 'red'}
    NOT_INFECTED_MARKER = 'o'                                 # Non-infected nodes show up as circles
    INFECTED_MARKER = 'X'                                     # Infected nodes appear as filled X markers
    GRAPH_DELAY = 1                                           # Time delay in seconds between graph updates

    # Indicies for the network file
    NETWORK_SOURCE_IP_INDEX = 0
    NETWORK_SINK_IP_INDEX = 1

    ###  Method functions
    
    def __init__(self, trafficPath, attackPath, networkPath, loadModels= False, epsilon= 1):
        """Class constructor
        Parameters
        ----------
        trafficPath
            String representing the file path to the dataset used for background messages

        attackPath
            String representing the file path to the dataset used for attack messages

        networkPath
            String representing the file path to the network parameters file

        loadModels
            Boolean describing whether previous models are loaded in for this game or new ones are initialized
            
        epsilon
            float from 0 to 1 representing the probability that each player makes random moves 

        Returns
        -------
        None
        """
        self.firstGame = True
        self.trafficPath = trafficPath
        self.attackPath = attackPath
        self.networkPath = networkPath
        self.loadModels = loadModels
        self.startingEpsilon = epsilon
        self.initializeGame()

    def initializeGame(self):
        """Initializes the starting game state, both players, and loads in the dataset
           Should be called after each game is played to prepare for the next one
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.colorMap = {}
        self.loadTrafficDataset(self.trafficPath)
        self.initializeNetwork(self.networkPath)
        
        if self.firstGame:
            self.firstGame = False
            self.attacker = Attacker(datasetPath= self.attackPath, networkSize= len(self.graph.nodes()), epsilon= self.startingEpsilon)
            self.defender = Defender(epsilon= self.startingEpsilon)
            if self.loadModels:
                self.attacker.loadModel()
                self.defender.loadModel()
        else:
            self.attacker.prepareForNextGame()
            self.defender.prepareForNextGame()
            
        
    def loadTrafficDataset(self, trafficPath):
        """loads in the dataset for generating background traffic
        Parameters
        ----------
        trafficPath
            String representing the file path to the dataset used for background traffic
        
        Returns
        -------
        None
        """
        self.dataset = pd.read_csv(trafficPath)

    def initializeNetwork(self, networkPath):
        """loads in the network parameters and creates a networkx graph
        Parameters
        ----------
        networkPath
            String representing the file path to the network parameters file
        
        Returns
        -------
        None
        """
        plt.ion()
        self.graph = networkx.DiGraph()
        with open(networkPath, 'r') as file:
            for line in file.readlines():
                elems = line.split(',')
                sourceIP = elems[GameEngine.NETWORK_SOURCE_IP_INDEX].strip()
                sinkIP = elems[GameEngine.NETWORK_SINK_IP_INDEX].strip()

                if not self.graph.has_node(sourceIP):
                    self.graph.add_node(sourceIP)
                    self.colorMap[sourceIP] = GameEngine.COLOR_MAP[Defender.NO_SUSPICION_LABEL]
                if not self.graph.has_node(sinkIP):
                    self.graph.add_node(sinkIP)
                    self.colorMap[sinkIP] = GameEngine.COLOR_MAP[Defender.NO_SUSPICION_LABEL]
                    self.
                self.graph.add_edge(sourceIP, sinkIP)

        allNodes = [node for node in self.graph.nodes()]
        self.infectedNodes = random.sample(allNodes, 1)
        self.shapeMap = {node : NOT_INFECTED_MARKER for node in allNodes}
        self.shapeMap[self.infectedNodes[0]] = INFECTED_MARKER
        self.reachableNodes = [int(self.isReachable(node)) for node in allNodes]
        self.quarantinedNodes = []

    def runGame(self):
        """Runs through one instance of the game,
           game ends when one player runs out of lives
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        while not self.gameOver():
           organizedQueues, trafficInfo, attckIndex = self.generateTrafficQueues()

            for queue in organizedQueues.values():
                for message in queue:
                    if random.random < self.calculateInspectionChance(len(queue)): continue            
                    suspicionLabel = self.defender.inspect(message)

                    self.updateNetwork(message, suspicionLabel)
                    reward = self.updateScore(message, suspicionLabel)

                    self.defender.addTrainingPoint(message, suspicionLabel, reward)
                    if message.isMalicious(): self.attacker.addTrainingPoint(trafficInfo, attackIndex, -reward)

                    print('Current message', message, ' was given a suspicion score of:', suspicionScore)
                    self.displayGraph()

    def gameOver(self):
        """Returns true if one player is out of lives"""
        return not any(self.reachableNodes)

    def generateTrafficQueues(self):
        """Fills the game queue with a random number of background messages,
           then randomly inserts the attack message into the queue
        Parameters
        ----------
        None
        
        Returns
        -------
        organizedQueues
            Dictionary with keys of node IPs and values representing the queue of message for that node

        trafficInfo
            Array containing information regarding each node about reachability, reward, and current traffic load
        
        attackIndex
            Integer representing the index in the set of graph nodes that is being attacked
        """
        self.traffic = self.generateBackgroundTraffic()
        organizedQueues = {node : [message for message in self.traffic if message.destination == node] for node in self.graph.nodes()}
        nodeInformation = [[len(organizedQueues[node]), node in self.reachableNodes, self.calculateNodeInfectionReward(node)] for node in self.graph.nodes()]
        trafficFlow, reachable, infectionScores = list(zip(*nodeInformation))
        attackMessage, attackIndex = self.attacker.getAttack(trafficFlow, reachable, infectionScores, self.infectedNodes, self.graph)
        if attackMessage != None:
            position = random.randint(0, len(organizedQueues[attack.destination]) + 1)
            organizedQueues[attackMessage.destination].insert(position, attackMessage)
        trafficInfo = (trafficFlow + reachable + infectionScores)
        return organizedQueues, trafficInfo, attackIndex

    def generateBackgroundTraffic(self):
        """Generate a random number of background messages from the dataset
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        messages = []
        numMessages = random.randint(1, GameEngine.MAX_BACKGROUND_TRAFFIC_MESSAGES)
        datasetLength = len(self.dataset.index)
        rowIndices = [random.randint(1, datasetLength - 1) for _ in range(numMessages)]
        rows = [list(self.dataset.iloc[index]) for index in rowIndices]
        for row in rows:            
            nodes = [node for node in self.graph.nodes()]
            row[Message.ORIGIN_INDEX] = random.choice(nodes)
            row[Message.DESTINATION_INDEX] = random.choice([node for node in nodes if self.graph.has_edge(newOrigin, node)])    # Pick destination as random node that it has a connection with
            messages.append(Message(row))
        return messages

    def calculateInspectionChance(self, queueLength):
        """Returns the probability of checking a message based on the size of the queue it's in
        """
        return 2.195 - (1 / (1 + math.exp(-.75 * queueLength))) - (1 / (1 + math.exp(-.05 *queueLength)))

    def updateNetwork(self, message, label):
        """Recolor the graph based on the new label

        Parameters
        ----------
        message
            message object that contains metadata about the message being inspected

       label
           String label representing the suspicion category the message falls into
        
        Returns
        -------
        None
        """
        self.colorMap[message.origin] = GameEngine.COLOR_MAP[label]
        if label == Defender.HIGH_SUSPICION_LABEL or Defender.MEDIUM_SUSPICION_LABEL:
            self.quarantineNode(message.origin, message.destination, label)

        if message.isMalicious() and (label != Defender.HIGH_SUSPICION_LABEL, label != Defender.MEDIUM_SUSPICION_LABEL):
            self.infectNode(message.destination)

        self.reachableNodes = [int(self.isReachable(node)) for node in self.graph.nodes()]

    def quarantineNode(self, origin, destination, label):
        """Remove outgoing edges from a node effectively hindering it from spreading infection
        Parameters
        ----------
        origin
            IP of the sender of the suspected infected message

        destination
            IP of the intended receipent of the suspected infected message

       label
           String label representing the suspicion category the message falls into
           Determines the strength of the quarantine
        
        Returns
        -------
        None
        """
        if origin not in self.quarantinedNodes and label == Defender.HIGH_SUSPICION_LABEL:
             self.quarantinedNodes.append(origin)
             for node in self.graph.nodes(): 
                 if self.graph.has_edge(origin, node): self.graph.remove_edge(node)
        else:
            self.graph.remove_edge(origin, destination)
    

    def infectNode(self, destination):
        """Marks a node as infected if not previously infectged
        Parameters
        ----------
        destination
            IP of the receipent of the infected message

        Returns
        -------
        None
        """
        if destination not in self.infectedNodes:
            self.infectedNodes.append(destination)
            self.shapeMap[destination] = INFECTED_MARKER 

    def calculateNodeInfectionReward(self, node):
        """Calculates reward for infecting the specified node
        Parameters
        ----------
        node
            node from the graph representing an IoT device

        Returns
        -------
        score
            integer value representing the degree of that node to other non-infected nodes
        """
        if node in self.infectedNodes: return 0 # No reward if currently impossible to infect
        score = 1
        for destination in self.graph.nodes():
            if graph.has_edge(node, destination) and destination not in self.infectedNodes:
                score += 1
        return score

    def isReachable(self, node):
        """Determines if a node is reachable for infection
        Parameters
        ----------
        node
            node from the graph representing an IoT device

        Returns
        -------
        reachable
            boolean value stating whether the node is reachable by the infected nodes
        """
        if node in self.infectedNodes:
            return False

        for infectedNode in infectedNodes:
            if self.graph.has_edge(infectedNode, node):
                return True

        return False

    def displayGraph(self):
        """Displays the current network colored by past suspicion scores"""

        networkx.draw_circular(self.graph, node_shape= self.shapeMap.values(), node_color= self.colorMap.values(), with_labels=True)
        plt.show()
        plt.pause(GameEngine.GRAPH_DELAY)

    def updateScore(self, message, label):
        """Calculates the reward earned for each player and updates lives
        Parameters
        ----------
        message
            message object that contains metadata about the message being inspected

       label
           String label representing the suspicion category the message falls into
        
        Returns
        -------
        None
        """
        possibleReward = self.calculateNodeInfectionReward(message.destination)
        if message.isMalicious() and label == Defender.HIGH_SUSPICION_LABEL:
            return possibleReward
        elif message.isMalicious() and label == Defender.MEDIUM_SUSPICION_LABEL:
            reward = possibleReward / 2
        elif message.isMalicious():
            reward = -possibleReward
        elif not message.isMalicious() and label ==  Defender.HIGH_SUSPICION_LABEL:
            reward = -possibleReward
        elif not message.isMalicious() and label == Defender.MEDIUM_SUSPICION_LABEL:
            reward = -possibleReward / 2
        elif not message.isMalicious():
            reward = possibleReward
        else:
            return 0

    def getSuspicionLabel(self, suspicionScore):
        """Calculates the reward earned for each player and updates live
        Parameters
        ----------
        message
            message object that contains metadata about the message being inspected

        suspicionScore
            float from 0 to 1 representing how certain probalisticly the defender things this message is malicious
        
        Returns
        -------
        None
        """
        label = Defender.NO_SUSPICION_LABEL 
        if suspicionScore > Defender..NO_SUSPICION_CUTOFF and suspicionScore <= GameEngine.LOW_SUSPICION_CUTOFF:
            label = Defender.LOW_SUSPICION_LABEL 
        elif suspicionScore > Defender.LOW_SUSPICION_CUTOFF and suspicionScore <= GameEngine.MEDIUM_SUSPICION_CUTOFF:
            label = Defender.MEDIUM_SUSPICION_LABEL 
        elif suspicionScore > Defender.MEDIUM_SUSPICION_CUTOFF:
            label = Defender.HIGH_SUSPICION_LABEL 
        
        return label

    def analyzeGameResults(self):
        """Return average degree, clustering coefficient, and connectedness of infected vs non-infected graph"""
        pass

    def train(self):
        """starts the training runs for each player
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.attacker.train()
        self.defender.train()
        self.attacker.saveModel()
        self.defender.saveModel()

if __name__ == "__main__":
    """Runs a specified number of games, training can be turned on via the train flag"""
    parser = argparse.ArgumentParser(description= 'Processes game parameters.')
    parser.add_argument('-ap', '--attackPath', type= str, default= "../datasets/defaultAttackDataset.csv", help= 'Path to the file of attack messages')
    parser.add_argument('-tp', '--trafficPath', type= str, default= "../datasets/defaultTrafficDataset.csv", help= 'Path to the file of background messages')
    parser.add_argument('-np', '--networkPath', type= str, default= "../networks/defaultNetwork.csv", help= 'Path to the file of network parameters for the game')
    parser.add_argument('-ep', '--episodes', type= int, default= 1, help= 'Number of games to be played')
    parser.add_argument('-t', '--train', action= 'store_true', help= 'Whether the agents should be training at the end of each game')
    parser.add_argument('-l', '--load', action= 'store_true', help= 'Whether previous models should be loaded in for this game')
    args = parser.parse_args()

    engine = GameEngine(trafficPath= args.trafficPath, attackPath= args.attackPath, networkPath= args.networkPath, loadModels= args.load)

    for episode in range(args.episodes):
        print('Starting episode', episode)
        engine.runGame()
        print('Episode', episode, 'complete')
        print('Post game analysis: ')
        engine.analyzeGameResults()
        if args.train:
            engine.train()
            print('Training for episode', episode, 'complete')
        engine.initializeGame()
