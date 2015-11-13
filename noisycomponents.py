import random

def allTuplesOfLength(x):
    if x == 0:
        return [()]

    else:
        oneLess = allTuplesOfLength(x-1)
        
        return [tuple([0]) + i for i in oneLess] + [tuple([1]) + i for i in oneLess]

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
    
    def __init__(self, inputs, output, tt, noise=0.001):
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
        
Ground = Wire()
Power = Wire()
Power.setValue(1)        
            
def And(inputs, output):        
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):0, (0,1):0, (1,0):0, (1,1):1})

def Or(inputs, output):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):0, (0,1):1, (1,0):1, (1,1):1})
    
def Nand(inputs, output):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):1, (0,1):1, (1,0):1, (1,1):0})
    
def Nor(inputs, output):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):1, (0,1):0, (1,0):0, (1,1):0})   
    
def Xor(inputs, output):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):0, (0,1):1, (1,0):1, (1,1):0})   
    
def Xnor(inputs, output):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):1, (0,1):0, (1,0):0, (1,1):1})       
    
def Maj3(inputs, output):
    assert len(inputs) == 3
    return LUT(inputs, output, {(0,0,0): 0,
                                (0,0,1): 0,
                                (0,1,0): 0,
                                (0,1,1): 1,
                                (1,0,0): 0,
                                (1,0,1): 1,
                                (1,1,0): 1,
                                (1,1,1): 1})
                                
def Xor3(inputs, output):
    assert len(inputs) == 3
    return LUT(inputs, output, {(0,0,0): 0,
                                (0,0,1): 1,
                                (0,1,0): 1,
                                (0,1,1): 0,
                                (1,0,0): 1,
                                (1,0,1): 0,
                                (1,1,0): 0,
                                (1,1,1): 1})
                                
def oneBitAdder(inputs, outputs):
    assert len(inputs) == 3
    assert len(outputs) == 2
    return Circuit(inputs, outputs, [Xor3(inputs, outputs[0]), Maj3(inputs, outputs[1])])

# Takes as input two n-bit numbers and returns a (n+1)-bit number    
def nBitAdder(numBits, inputs, outputs):
    assert len(inputs) == 2*numBits
    assert len(outputs) == numBits+1
    
    global Ground
    
    listOfLittleAdders = []
 
    for i in range(numBits-1, -1, -1):
        if i == numBits-1:
            # first one has no carry-in
            carryIn = Ground
        
        if i == 0:
            carryOut = outputs[0]
        else:    
            carryOut = Wire()
             
        firstInput = inputs[i]
        secondInput = inputs[i+numBits]
        thirdInput = carryIn
        output = outputs[i+1]
            
        listOfLittleAdders.append(oneBitAdder([firstInput, secondInput, thirdInput], \
            [output, carryOut]))
            
        carryIn = carryOut
        
    return Circuit(inputs, outputs, listOfLittleAdders)        
        
        
firstInputs = Bus(4)
secondInputs = Bus(4)

inputs = firstInputs.merge(secondInputs)
outputs = Bus(5)
                                            
adder = nBitAdder(4, inputs, outputs)

firstInputs.setValue((0,1,1,0))
secondInputs.setValue((1,1,0,1))

adder.evaluate()

print outputs