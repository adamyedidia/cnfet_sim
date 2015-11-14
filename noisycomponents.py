import random

def STANDARD_NOISE():
    return 0.001


def POWER_ERROR_TRADEOFF(noise):
    # Totally made up
    return 1./noise  

class Wire:
    def __init__(self):
        self.v = 0
        
    def __str__(self):
        return str(self.v) + "v "    
        
    def setValue(self, newVoltage):
        self.v = newVoltage

class Bus:
    def __init__(self, numWires=0, listOfWires=None):
        if listOfWires == None:
            self.listOfWires = []
        
            for i in range(numWires):
                self.listOfWires.append(Wire())
                
        else:
            self.listOfWires = listOfWires
            
    def __getitem__(self, index):
        return self.listOfWires[index]
        
    def __str__(self):
        returnString = ""
        
        for wire in self.listOfWires:
            returnString += str(wire)
            
        return returnString
            
    def __len__(self):
        return len(self.listOfWires)
                    
    def merge(self, otherBus):
        newListOfWires = self.listOfWires + otherBus.listOfWires
        
        return Bus(len(newListOfWires), newListOfWires)                
                    
    def setValue(self, newVoltages):
        for i, voltage in enumerate(newVoltages):
            self.listOfWires[i].setValue(voltage)

class LUT:
    global NUM_INPUTS
    
    def __init__(self, inputs, output, tt, noise=STANDARD_NOISE()):
        self.inputs = inputs
        self.output = output
        self.tt = tt
        self.noise = noise
        
    def extractInputs(self):
        return tuple([w.v for w in self.inputs])
        
    def evaluate(self):
        if random.random() >= self.noise:
            self.output.setValue(self.tt[self.extractInputs()])
        else:
            self.output.setValue(1 - self.tt[self.extractInputs()])
        
    def countGates(self):
        return 1    
        
    def powerConsumption(self):
        return POWER_ERROR_TRADEOFF(self.noise)
        
class Circuit:
    def __init__(self, inputs, outputs, listOfSubcircuits):
        # inputs is a list of Wires
        # output is a list of Wires
        
        self.inputs = inputs
        self.outputs = outputs
        
        # A list of Circuits and LUTs
        self.listOfSubcircuits = listOfSubcircuits
        
    def evaluate(self):
        for subcircuit in self.listOfSubcircuits:
            subcircuit.evaluate()
            
    def countGates(self):
        numGates = 0
        for subcircuit in self.listOfSubcircuits:
            numGates += subcircuit.countGates()
            
        return numGates
        
    def powerConsumption(self):
        totalPower = 0.0
        for subcircuit in self.listOfSubcircuits:
            totalPower += subcircuit.powerConsumption()
            
        return totalPower