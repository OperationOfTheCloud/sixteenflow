from bitarray import bitarray
import math

class Ternary:
    """
    A memory-efficient array-like class to store ternary values (-1, 0, 1).
    Each value is stored using 2 bits.
    - 0 is stored as '00'
    - 1 is stored as '01'
    - -1 is stored as '10'
    """
    _INT_TO_BITS = {0: bitarray('00'), 1: bitarray('01'), -1: bitarray('10')}
    _BITS_TO_INT = {'00': 0, '01': 1, '10': -1}

    def __init__(self, data):
        """
        Initializes the Ternary array.
        :param data: An integer specifying the size of the array (initialized to zeros),
                     or a list/tuple of integers (-1, 0, 1).
        """
        if isinstance(data, int):
            self.size = data
            self._bits = bitarray(self.size * 2)
            self._bits.setall(0)
        elif isinstance(data, (list, tuple)):
            self.size = len(data)
            self._bits = bitarray()
            for val in data:
                if val not in self._INT_TO_BITS:
                    raise ValueError(f"Invalid ternary value: {val}. Must be -1, 0, or 1.")
                self._bits.extend(self._INT_TO_BITS[val])
        else:
            raise TypeError("Argument must be an int (size) or a list/tuple of ternary values.")

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        if index < 0:
            index += self.size
        if not 0 <= index < self.size:
            raise IndexError("Ternary array index out of range")
        
        start = index * 2
        bit_pair = self._bits[start:start+2].to01()
        return self._BITS_TO_INT.get(bit_pair, 0) # Default to 0 for safety

    def __setitem__(self, index, value):
        if value not in self._INT_TO_BITS:
            raise ValueError(f"Invalid ternary value: {value}. Must be -1, 0, or 1.")
        if index < 0:
            index += self.size
        if not 0 <= index < self.size:
            raise IndexError("Ternary array index out of range")
            
        start = index * 2
        self._bits[start:start+2] = self._INT_TO_BITS[value]

    def __repr__(self):
        values = [str(self[i]) for i in range(self.size)]
        return f"Ternary([{', '.join(values)}])"

    def to_list(self):
        return [self[i] for i in range(self.size)]

# Example Usage:
# my_weights = Ternary([-1, 0, 1, 1, 0, -1, 0, 0, 1])
# print(my_weights)
# print(f"Value at index 2: {my_weights[2]}")
# my_weights[2] = -1
# print(f"New value at index 2: {my_weights[2]}")
# print(f"Memory size of underlying bitarray: {my_weights._bits.buffer_info()[1]} bytes")
# print(f"Underlying bits: {my_weights._bits.to01()}")
