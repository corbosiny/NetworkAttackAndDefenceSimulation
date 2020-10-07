class Message():

    ### Static class Variables

    # Message label categories
    MALICIOUS_LABEL = "Malicious"
    BENIGN_LABEL = "Benign"

    # Metadata index variables
    ORIGIN_INDEX = 0
    LABEL_INDEX = 1

    ### Member functions

    def __init__(self, args):
        """Class constructor
        Parameters
        ----------
        args
            An array containing message metadata organized as follows:
            
            origin
                String with the IP address of the originating node

            label
                String representing whether the message is malicious or benign
            
        Returns
        -------
        None
        """
        self.origin = args[Message.ORIGIN_INDEX]
        self.label = args[Message.LABEL_INDEX]

    def isMalicious(self):
        """Returns a boolean flag stating whether the message is malicious"""
        return self.label == Message.MALICIOUS_LABEL

    def asNetworkInputs(self):
        """Returns the message metadata as an array to be fed into networks
        Parameters
        ----------
        None
        
        Returns
        -------
        Metadata array containing these elements:
            origin
                String with the IP address of the originating node

        """
        return [self.origin]

    def __str__(self):
        """Returns a string of the message metadata when an attempt to turn a message object into a string occurs"""
        args = self.asNetworkInputs()
        args.append(self.label)
        string = ','.join(args)
        return string

if __name__ == "__main__":
    args = ["127.0.0.0.1", Message.BENIGN_LABEL]
    message = Message(args)
    print(message.origin)
    print(message.label)
    print(message.isMalicious())
    print(message.asNetworkInputs())
    print(message)