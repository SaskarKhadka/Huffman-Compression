from node import Node
from merge_sort import merge_sort
from bitarray import bitarray


class Huffman:

    """
    A class that encapsulates all the functionalities related 
    to text compression and decompression using Huffman Coding 

    ...

    Attributes
    ----------
    freq_table : dict
        table that records the frequency of charcters in original text
    leaf_nodes : list
        list of nodes of charcters which occur in the original text
    code_table : dict
        table that records the code for each character in the freq_table
    padding : int
        bits required to create a round byte in the compressed file
    root: Node
        root of the huffman heap

    Methods
    -------
    compress(file_data)
        Encodes the original text to binary

    decompress(utils, file)
        Decodes the compressed binary to original text using utils(code table)

    create_frequency_table(file_data)
        Creates frequency table for characters occuring in the original text

    create_code_table(root, code="", parent=None)
        Creates code table for characters occuring in the original text

    create_heap()
        Creates a maximum heap using the Nodes in leaf_nodes
    """

    def __init__(self) -> None:
        self.freq_table = {}
        self.leaf_nodes = []
        self.code_table = {}
        self.padding = 0
        self.root = None

    def compress(self, file_data):
        '''
        Encodes the original text to binary
        '''

        self.create_frequency_table(file_data)
        self.create_heap()
        temp = self.root
        self.create_code_table(root=temp)

        code_table_bits = {key: bitarray(value)
                           for key, value in self.code_table.items()}
        encoded = bitarray()
        encoded.encode(code_table_bits, file_data)
        self.padding = 8 - len(encoded) % 8

        return {"encoded": encoded,
                "utils": {"padding": self.padding,
                          "code": self.code_table
                          }}

    def decompress(self, utils, file):
        '''
        Decodes the compressed binary to original text using utils(code table)
        '''

        decoded = bitarray()
        decoded.fromfile(file)

        decoded = decoded[:-utils['padding']]

        code_table_bits = {key: bitarray(value)
                           for key, value in utils["code"].items()}

        decoded = decoded.decode(code_table_bits)

        decoded = "".join(decoded)
        return decoded

    def create_frequency_table(self, file_data):
        '''
        Creates frequency table for characters occuring in the original text
        '''

        for char in file_data:
            self.freq_table[char] = self.freq_table[char] + \
                1 if (char in self.freq_table) else 1

        self.leaf_nodes = [Node(key, value)
                           for key, value in self.freq_table.items()]

    def create_heap(self):
        '''
        Creates a maximum heap using the Nodes in leaf_nodes
        '''

        freq_table_copy = self.leaf_nodes
        while len(freq_table_copy) != 1:
            merge_sort(freq_table_copy)
            first = freq_table_copy[0]
            second = freq_table_copy[1]
            root = Node(None, first.freq + second.freq)
            root.right = first
            root.left = second
            freq_table_copy = freq_table_copy[2:]
            freq_table_copy.insert(0, root)
        self.root = freq_table_copy.pop(0)

    def create_code_table(self, root, code="", parent=None):
        '''
        Creates code table for characters occuring in the original text
        '''

        if (root is None):
            self.code_table[parent.value] = code
            return

        self.create_code_table(root.left, code +
                               "0" if root.value is None else code, parent=root)
        self.create_code_table(root.right, code +
                               "1" if root.value is None else code, parent=root)
