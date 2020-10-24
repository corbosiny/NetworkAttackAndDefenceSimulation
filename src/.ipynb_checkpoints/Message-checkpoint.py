class Message():

    ### Static class Variables

    # Message label categories
    MALICIOUS_LABEL = "Malicious"
    BENIGN_LABEL = "Benign"

    # Metadata index variables
    ORIGIN_INDEX = 3
    DESTINATION_INDEX = 6
    LABEL_INDEX = 14
    TOTPKTS_INDEX = 11
    TOTBYTES_INDEX = 12
    SRCBYTES_INDEX = 13
    DUR_INDEX = 2
    ### Member functions

    def __init__(self, args):
        """Class constructor
        Parameters
        ----------
        args
            An array containing message metadata organized as follows:
            
            origin
                String with the IP address of the originating node

            destination
                String with the IP address of the destination node

            label
                String representing whether the message is malicious or benign
            
        Returns
        -------
        None
        """
        self.origin = args[Message.ORIGIN_INDEX]
        self.destination = args[Message.DESTINATION_INDEX]
        self.label = args[Message.LABEL_INDEX]
        self.totpkts = args[Message.TOTPKTS_INDEX]
        self.totbytes = args[Message.TOTBYTES_INDEX]
        self.srcbytes = args[Message.SRCBYTES_INDEX]
        self.dur = args[Message.DUR_INDEX]
        
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
            
            destination
                String with the IP address of the destination node

        """
        #return [self.origin, self.destination]
        return [self.dur, self.srcbytes, self.totbytes, self.totpkts]

    def __str__(self):
        """Returns a string of the message metadata when an attempt to turn a message object into a string occurs"""
        args = self.asNetworkInputs()
        args = [self.origin, self.destination, self.label] + args
        args = [str(arg) for arg in args]
        string = ','.join(args)
        return string

if __name__ == "__main__": 
    args = ['','','800', "127.0.0.0.1", '', '', '196.62.0.1', '', '', '', '', '1','10','100', Message.MALICIOUS_LABEL]
    message = Message(args)
    print(message.origin)
    print(message.destination)
    print(message.label)
    print(message.isMalicious())
    print(message.asNetworkInputs())
    print(message)
