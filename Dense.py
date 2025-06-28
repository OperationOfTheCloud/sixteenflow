from BitType import Ternary

class Dense:
    def __init__(self, Input, Output):
        self.Biases = Ternary([0] * Input)
        self.Weights = [Ternary([0] * Input)] * Output
    def Predict(self, Inputs):
        self.Inputs = Inputs
        