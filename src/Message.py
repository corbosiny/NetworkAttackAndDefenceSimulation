class Message():

    MALICIOUS_LABEL = "Malicious"
    BENIGN_LABEL = "Benign"

    def __init__(self, origin, label):
        """Class constructor
        Parameters
        ----------
        origin
            String with the IP address of the originating node

        label
            String representing whether the message is malicious or benign
        
        Returns
        -------
        None
        """
        self.origin = origin
        self.label = label

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

if __name__ == "__main__":
    message = Message("127.0.0.0.1", Message.MALICIOUS_LABEL)
    print(message.origin)
    print(message.label)
    print(message.isMalicious())
    print(message.asNetworkInputs())