# Pyhton Libraries
import argparse
import networkx
import random
import pandas as pd
import matplotlib.pyplot as plt

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

    MAX_BACKGROUND_TRAFFIC_MESSAGES = 5      # The maximum number of background messages between attacks
    
    # Thresholds for the suspicion score 
    NO_SUSPICION_CUTOFF     = .1                                       # Any messages below this threshold are considered not suspicous                                       
    LOW_SUSPICION_CUTOFF  = .35                                   # Any messages inside this threshold are still considered not suspicous but are colored differently
    MEDIUM_SUSPICION_CUTOFF = .6                              #  Any messages inside this threshold are considered  flagged but not ouright rejected

    # Colorings for suspicion scores
    NO_SUSPICION_LABEL = 'NONE'
    LOW_SUSPICION_LABEL = 'LOW'
    MEDIUM_SUSPICION_LABEL = 'MEDIUM'
    HIGH_SUSPICION_LABEL = 'HIGH'

    COLOR_MAP = {NO_SUSPICION_LABEL  : 'blue'. LOW_SUSPICION_LABEL  : 'yellow', MEDIUM_SUSPICION_LABEL :  'orange', HIGH_SUSPICION_LABEL : 'red'}

    ###  Method functions
    
    def __init__(self, datasetPath, networkPath, load= False, epsilon= 1):
        """Class constructor
        Parameters
        ----------
        datasetPath
            String representing the file path to the dataset used for background traffic

        networkPath
            String representing the file path to the network parameters file

        load
            Boolean describing whether previous models are loaded in for this game or new ones are initialized
            
        epsilon
            float from 0 to 1 representing the probability that each player makes random moves 

        Returns
        -------
        None
        """
        self.datasetPath = datasetPath
        self.networkPath = networkPath
        self.load = load
        self.startingEpsilon = epsilon
        self.loadDataSet()
        self.initializeGame()
        self.firstGame = True

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
        self.queue = []
        self.turnHistory = []
        self.loadDataset
        self.initializeNetwork(self.networkPath)
        
        if self.firstGame:
            self.firstGame = False
            self.attacker = Attacker(epsilon= self.startingEpsilon)
            self.defender = Defender(epsilon= self.startingEpsilon)
            if self.load:
                self.attacker.loadModel()
                self.self.defender.loadModel()
        else:
            self.attacker.prepareForNextGame()
            self.defender.prepareForNextGame()
            
        
    def loadDataset(self, datasetPath):
        """loads in the dataset for generating background traffic
        Parameters
        ----------
        datasetPath
            String representing the file path to the dataset used for background traffic
        
        Returns
        -------
        None
        """
        self.dataset = pd.read_csv(datasetPath)

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
        self.graph = networkx.graph()
        with open(networkPath, 'r') as file:
            for line in file.readlines():
                #TODO:
                # add node to graph
                # add color map index to be blue
                self.graph[message.origin] = GameEngine.COLOR_MAP[NO_SUSPICION_LABEL]
                
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
            self.updateQueue()
            for message in self.queue:
                suspicionScore = self.defender.inspect(message)
                label = self.getSuspicionLabel(suspicionScore)
                self.updateGraph(message, label)
                reward = self.updateScore(message, label)

                self.defender.addTrainingPoint(message, suspicionScore, reward)
                if message.isMalicious(): self.attacker.addTrainingPoint(message, suspicionScore, -reward)

            self.displayGraph()
        
    def self.gameOver(self):
        """Returns true if one player is out of lives"""
        return self.defender.lives == 0 or self.attacker.lives == 0

    def updateQueue(self):
        """Fills the game queue with a random number of background messages,
           then randomly inserts the attack message into the queue
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        messages = self.generateBackgroundTraffic()
        attack = self.attacker.getAttack()
        position = random.randint(0, len(messages) + 1)
        messages.insert(attack, position)
        for message in messages:
            self.queue.append(message)

    def generateBackgroundTraffic(self):
        """Generate a random number of background messages from the dataset
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
        # TODO:
        # return random number of background traffic messages
        # make message class
        # decide on features for message
        numMessages = random.randint(0, GameEngine.MAX+BACKGROUND_TRAFFIC_MESSAGES)
        messages = []
        for i in range(numMessages):
            #TODO:
            # make message object
            # grab random traffic
            pass
        return messages

    def updateGraph(self, message, label):
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
        # TODO:
        # map suspicion score to color
        # recolor node based off message IP
        self.colorMap[message.origin] = GameEngine.COLOR_MAP[label]


    def displayGraph(self):
        """Displays the current network colored by past suspicion scores"""
        nx.draw(self.graph, node_color=self.colorMap, with_labels=True)
        plt.show()

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
        reward = 0
        if message.isMalicious() and label == GameEngine.HIGH_SUSPICION_LABEL :
            self.attacker.lives -= 1
            reward = 10
        elif message.isMalicious() and label == GameEngine.MEDIUM_SUSPICION_LABEL :
            reward = 5
        elif message.isMalicious():
            self.defender.lives -= 1
            reward = -10
        elif not message.isMalicious() and label ==  GameEngine.HIGH_SUSPICION_LABEL :
            self.defender.lives -= 1
            reward = -10
        elif not message.isMalicious() and label == GameEngine.MEDIUM_SUSPICION_LABEL :
            reward = 0
        elif not message.isMalicious():
            reward = 10
        return reward

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
        label = GameEngine.NO_SUSPICION_LABEL 
        if suspicionScore > GameEngine.NO_SUSPICION_SCORE and suspicionScore <= GameEngine.LOW_SUSPICION_CUTOFF:
            label = GameEngine.LOW_SUSPICION_LABEL 
        elif suspicionScore > GameEngine.LOW_SUSPICION_SCORE and suspicionScore <= GameEngine.MEDIUM_SUSPICION_CUTOFF 
            label = GameEngine.MEDIUM_SUSPICION_LABEL 
        elif  suspicionScore > GameEngine.MEDIUM_SUSPICION_CUTOFF:
            label = GameEngine.HIGH_SUSPICION_LABEL 
        
        return label

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
    parser.add_argument('-dp', '--dataPath', type= str, default= "../datasets/defaultDataset.txt", help= 'Path to the file of network parameters for the game')
    parser.add_argument('-np', '--networkPath', type= str, default= "../networks/defaultNetwork.txt", help= 'Path to the file of network parameters for the game')
    parser.add_argument('-ep', '--episodes', type= int, default= 1, help= 'Number of games to be played')
    parser.add_argument('-t', '--train', action= 'store_true', help= 'Whether the agents should be training at the end of each game')
    parser.add_argument('-l', '--load', action= 'store_true', help= 'Whether previous models should be loaded in for this game')
    args = parser.parse_args()

    engine = GameEngine(datasetPath= args.dataPath, networkPath= args.networkPath, load= args.load)

    for episode in range(args.episodes):
        print('Starting episode', episode)
        engine.runGame()
        print('Episode', episode, 'complete')
        if args.train:
            engine.train()
            print('Training for episode', episode, 'complete')
        engine.initializeGame()
