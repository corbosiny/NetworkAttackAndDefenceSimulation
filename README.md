# Getting Started

This readme will take you through how to get this repo up and running with the example agents, make your own datasets, and also how to create your own versions of the attacker and defender. 
Along side this readme each function in the source code has a header explaining its use, inputs, and return values. Lastly, in the GameEngine code at the bottom is a detailed 

---
## Installing Dependancies

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

To double check that the game files were properly set up the example agent can be run. cd into the src directory. Then either run the following command on your terminal of choice:

`python3 GameEngine.py`
---
## Parameters to run the GameEngine

There are a set of parameters that can be tacked on when running the GameEngine. Each of these parameters has a default value that can be observed by looking at the argparser code at the bottom of the GameEngine.py file. The full list of parameters and their descriptions is shown below:

-ap, attackPath -- String file path to the csv file containing the attack message metadata, see examples in the datasets folder 
-tp, trafficPath -- String file path to the csv file containing the background traffic message metadata, see examples in the datasets folder 
-np, networkPath -- String file path to the csv file containing the attack message metadata, see examples in the datasets folder 
-ep, episodes -- Integer representing the number of episodes that will be played
-t, train -- Boolean, if this flag is set both models will train after each episode and a training log will be created
-l, load -- Boolean, if this flag is set new models won't be initialized, past models will be loaded in. These models are saved under local_models in individual named folders
-nv, noVisualize -- Boolean, if this flag is called the visualization will be turned off
---
## Agent class

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

---

### Training Checkpoints

A training episode consists of one play through of a game between the Attacker and Defender, a game is over when the attacker can no longer reach any non-infected nodes. Once post game training is complete a checkpoint will be made by Agent.py in order to save the model for later use. As well custom training logs will be made for each unique class, in this case only Attacker and Defender, that will show the training error of the Agent as it is learning. These logs and models are stored in the logs and models directories respectively and are formatted as local_models/{class_name}Models/. and local_logs/{class_name}{Log}. Note that the formatting is based on the class name and so only one instance of a model for each unique class can be stored as of now. Furthermore a gitignore inside each of these folders prevents them from being tracked by git unless moved to another folder to avoid frequent merge conflicts when separate users who are training models push to the same branch.

---

## Message Class

### Datasets

### How to extract useful info

---

## Attacker Class

### Current Features

### Dataset

### How to implement your own


## Defender

### Current Features

### Dataset

### How to implement your own
---
