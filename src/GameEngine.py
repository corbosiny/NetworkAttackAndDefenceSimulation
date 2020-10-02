import argparse
import networkx
import random
import pandas as pd
#from Attacker import Attacker
#from Defender import Defender

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
    
    def __init__(self, datasetPath, networkPath):
        """Class constructor

        Parameters
        ----------
        datasetPath
            String representing the file path to the dataset used for background traffic

        networkPath
            String representing the file path to the network parameters file
            
        Returns
        -------
        None
        """
        self.datasetPath = datasetPath
        self.networkPath = networkPath
        self.loadDataSet()
        self.initializeGame()
        self.firstGame = True

    def initializeGame(self, load= False):
        """Initializes the starting game state, both players, and loads in the dataset
           Should be called after each game is played to prepare for the next one

        Parameters
        ----------
        load
            Boolean stating whether or not to load existing models for the next game
        
        Returns
        -------
        None
        """
        self.queue = []
        self.loadDataset
        self.initializeNetwork(self.networkPath)
        if self.firstGame:
            self.firstGame = False
            self.attacker = Attacker()
            self.defender = Defender()

        if load:
            self.attacker.loadModel()
            self.defender.loadModel()
        
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
                pass
        
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
                self.updateGraph(message, suspicionScore)
                self.updateScore(message, suspicionScore)

        self.attacker.saveModel()
        self.defender.saveModel()
        
    def self.gameOver(self):
        """Returns true if one player is out of lives"""
        return self.defender.lives == 0 || self.attacker.lives == 0

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
        # TODO:
        # return random number of background traffic messages
        # make message class
        # decide on features for message
        pass

    def updateGraph(self, message, suspicionScore):
        # TODO:
        # map suspicion score to color
        # recolor node based off message IP
        pass

    def updateScore(self, message, suspicionScore):
        # TODO:
        # map score to fuzzy membership values
        # check if correct labeling
        # update lives
        pass

    def train(self):
        # TODO:
        # Come up with method of saving and loading models
        # train models
        # write checkpoints and logs
        # add game memory
        pass

if __name__ == "__main__":
    """Runs a specified number of games, training can be turned on via the train flag"""
    
    parser = argparse.ArgumentParser(description= 'Processes game parameters.')
    parser.add_argument('-dp', '--dataPath', type= str, default= "../networkFiles/defaultNetwork.txt", help= 'Path to the file of network parameters for the game')
    parser.add_argument('-np', '--networkPath', type= str, default= "../networkFiles/defaultNetwork.txt", help= 'Path to the file of network parameters for the game')
    parser.add_argument('-ep', '--episodes', type= int, default= 1, help= 'Number of games to be played')
    parser.add_argument('-t', '--train', action= 'store_true', help= 'Whether the agents should be training at the end of each game')
    args = parser.parse_args()

    engine = GameEngine(datasetPath= args.dataPath, networkPath= args.networkPath)

    for episode in range(args.episodes):
        print('Starting episode', episode)
        engine.runGame()
        print('Episode', episode, 'complete')
        if args.train:
            engine.train()
            print('Training for episode', episode, 'complete')
