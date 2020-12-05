# Getting Started

This readme will take you through how to get this repo up and running with the example agents, make your own datasets, and also how to create your own versions of the attacker and defender. 
Along side this readme each function in the source code has a header explaining its use, inputs, and return values. Lastly, in the GameEngine code at the bottom is a detailed 

---
## Installing Dependancies
This section is for anyone running this project localy on your machine. If you wish to skip this section, which is recommended, instead clone this project to a Google Collab project and the baseline dependancies should already work. Or you can use the provide Google Collab project: https://colab.research.google.com/drive/1NWNoH0t0w3wWuPwV0FkD57FzDAtTk-Cj?usp=sharing

If running on linux please update and upgrade your current distro:
`sudo apt-get update`  
`sudo apt-get upgrade` 

This code only works with Python 3.7, we recommend Python 3.7.2. Before trying to install dependencies it is recommend to open a command line interface of choice inside the repo and run:   
`pip install --upgrade pip`  

or if you have Python2 and 3 installed:  
`pip3 install --upgrade pip` 

To download the necessary dependencies after cloning the repo call:  
`pip install -r requirements.txt`

or if you have Python2 and 3 installed:  
`pip3 install --upgrade pip` 

This should be called in the top level directory of the repo. This will install the following libraries you will need to create game environments that serve as a wrapper abstracting the interface between your agent and the underlying emulator:

-tensorflow  
-networkx   
-matplotlib  
-numpy  
-pandas  
-scipy  
-keras  

These libraries can sometimes have serious issues installing themselves or their dependencies on a windows machine, this usually can be tied to not having the correct version of python installed.

---
## The first test run

To double check that the game files were properly set up the GameEngine can be run on a default dataset. If running locally cd into the src directory. Then either run the following command on your terminal of choice:

`python GameEngine.py`

or if you are running it in a Google Collab Project:  
`!python3 GameEngine.py`

The GameEngine is essentially the main file and all simulations will be run by calling this script with the desired parameters.
---
## Parameters to run the GameEngine

Each of the engine parameters have a default value that can be observed by looking at the argparser code at the bottom of the GameEngine.py file. The full list of parameters and their descriptions is shown below.

`-ap, --attackPath`, String file path to the csv file containing the attack message metadata, see examples in the datasets folder     
`-tp, --trafficPath`, String file path to the csv file containing the background traffic message metadata, see examples in the datasets folder    
`-np, --networkPath`, String file path to the csv file containing the csv edge list to represnt the network, see examples in the networks folder. These can be generated via scripts or exported from programs like gephi    
`-ep, --episodes`, Integer representing the number of episodes that will be played    
`-t, --train`, Boolean, if this flag is set both models will train after each episode and a training log will be created    
`-l, --load`, Boolean, if this flag is set new models won't be initialized, past models will be loaded in. These models are saved under local_models in individual named folders    
`-nv, --noVisualize`, Boolean, if this flag is called the visualization will be turned off    
---
## Building your own simulation

In order to implement different underlying models for the attacker and defender there are few key parts of the code that need to be modified. Each class in the source code will discussed below and the parts that need to be edited will be discussed. Alongside these descriptions every function has detailed comments that can be read for further insight within the source code.

### Agent class

The Agent class serves as a template from which the RL models can inherit from. It implements several background bookkeeping functions such as saving/loading models, preparing memory for the next game, and making training logs.

There are three main functions that need to be implemented by the attacker or defender after they inherit from Agent:

-initializeNetwork  
-addTrainingPoint  
-trainModel

Each section below gives a description of the interface required for each function and it's purpose. Further documentation can be seen inside the code of Agent.py

#### initializeNetwork

initializeNetwork creates a keras model and is expected to set the self.model object variable with that model. The size does not matter as the Agent fucntions can save and load the model without knowing specifics about the model. If the load flag is set then a pretrained model will be loaded instead by the background Agent functions and this function will not be called. It does not take in any parameters.

#### addTrainingPoint

Adds one training point to the agents memory to review after the game. This is called after each decision made by the agent and is a chance to format each training point as desired before training happens after the game. Each training point should be paired with the decision the Agent made along with it's reward, which are all fed into this function, as they are being trained using Q reinforcement learning. An example of this function implemented can be seen in the Attacker.py and Defender.py files.

#### trainNetwork

Uses the training data stored in the memory object variable during training and the current model and runs one training epoch on it. This function is called after each episode if the training flag is set.

#### Training Checkpoints

A training episode consists of one play through of a game between the Attacker and Defender, a game is over when the attacker can no longer reach any non-infected nodes. Once post game training is complete a checkpoint will be made by Agent.py in order to save the model for later use. Ccustom training logs will be made for each unique class, in this case only Attacker and Defender, that will show the training error of the Agent as it is learning. These logs and models are stored in the logs and models directories respectively and are formatted as local_models/{class_name}Models/. and local_logs/{class_name}{Log}. Note that the formatting is based on the class name and so only one instance of a model for each unique class can be stored as of now. Furthermore a gitignore inside each of these folders prevents them from being tracked by git unless moved to another folder to avoid frequent merge conflicts when separate users who are training models push to the same branch.

### Message Class

The message data is a wrapper around the set of mesage meta data corresponding to one captured message from the datasets. This class is the interface that the Attacker and Defender use to formulate simulated messages and attacks. A set of static variables representing the indicies of the metadata to be used is contained at the top of the class. If different datasets are going to be used for these simulations then these variables need to be modified to reflect the new capture data. However the final argument should always be the truth label of the message; Benign or Malicious. The only function that would also need to change is the asNetworksInputs function that returns the useful metadata as an array to be input to a neural network. This should return the formatted information that the Attacker and the Defender will both be using from the message.


### Attacker and Defender Class

Aside from implementing the three specified functions discussed in the Agent class, the remaing functions inside of these classes implement formatting messages from network outputs or discretizing suspicion labels. So the functions inside of these classes should work for any type of attacker, defender, or network you are trying to model outside of the three functions inherited from Agent that must be implemented.

### GameEngine

Finally in GameEngine there are four main functions that need to be changed in order to influence how the game effectively plays. The rest are bookkeeping functions that manage the background handling of the simulation and loading in datasets. The four functions are:

-calculateInspectionChance  
-generateBackgroundTraffic  
-calculateNodeInfectionReward  
-calculateScore  

#### Calculate Inspection Chance

This function takes in the size of the traffic buffer to one node and calculates the chance that a given message is inspected or slipped through. In our implementation the more messages backedup the more that slip through without being properly inspected. This could be altered to enforce total inspection or to allow for a variety of techniques that influence inspection chance. All that needs to be returned is a floating point value representing the probability for a nodes inspection chance.

#### Generate Background Traffic

This generates the random benign messages that flow through the network. In our implementation the source and destination of a message are chosen at random but this could be changed to follow more realistic temporal models where flow rate can change depending on certain time frames or that nodes with higher degrees have a higher chance of being selected as the source for out going messages. Several different techniques could be used to model simulation traffic here. All that is required is a dictionary mapping each nodes name to it's traffic buffer is required to be returned.

#### Calculate Node Infection Reward

This function determines how useful a node is to infect for the attacker. In our implementation the number of newly introduced connections to non-infected nodes achieved by infecting this node is the reward. The idea is to target the nodes that maximize cross boundary connections. Other implementations such as going after nodes with high betweeness centrality could be targeted as well.

#### Calculate Score

A message and the defenders label are input into this function and the score for both sides is returned. Now if the message is not malicious no score is returned for the attacker as it did not take part in this decision. In our implementation the defender is penalized/rewarded based upon the degree of the node that it is effected by its decision. The idea is to try to be more careful in defending nodes that are more crucial to the network in terms of centrality so that the network stays efficient. If the node is quarantined while being innocent that induces a penalty while if the node was infected it is rewarded. Various weightings could be applied to how the defender is rewarded/penalized here based upon how many nodes are cutoff if this node were to be infected/quarantined.

---
