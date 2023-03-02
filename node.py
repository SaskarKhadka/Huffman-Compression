class Node:
    """
    A class that encapsulates the attributes 
    related to a Node in tree data structure 

    ...

    Attributes
    ----------
    value : str
        value of the node i.e character in the original text
    freq : int
        frequency of occurence of the value in the original text
    left : Node
        left child of the Node
    right : Node
        right child of the Node

    """

    def __init__(self, val, freq=1) -> None:
        self.value = val
        self.freq = freq
        self.left = None
        self.right = None
