from noisycomponents import *
from basicgates import *

import random
import matplotlib.pyplot as p

def ERROR_PUNISHMENT(trueValue, ourValue):
    return (trueValue - ourValue) ** 2

def convertNumberToBits(x, numBits):
    
    if numBits == 0:
        return tuple([])
        
    elif x >= 2**(numBits-1):
        return tuple([1]) + convertNumberToBits(x%(2**(numBits-1)), numBits-1)
    else:
        return tuple([0]) + convertNumberToBits(x%(2**(numBits-1)), numBits-1)
        
def convertBitsToNumber(bits):
        
    if len(bits) == 0:
        return 0    
        
    elif bits[-1].v == 1:
        return 1 + 2*convertBitsToNumber(bits[:-1])
        
    else:
        return 2*convertBitsToNumber(bits[:-1])


# returns (power consumption, average error)                
def adderTest(numBits, numIterations, noiseFunction):
    firstInputs = Bus(numBits)
    secondInputs = Bus(numBits)

    inputs = firstInputs.merge(secondInputs)
    outputs = Bus(numBits+1)
                                            
    adder = nBitAdder(numBits, inputs, outputs, noiseFunction)
    
    totalError = 0
    
    for _ in range(numIterations):
        for number1 in range(2**numBits):
            for number2 in range(2**numBits):
                bits1 = convertNumberToBits(number1, numBits)
                bits2 = convertNumberToBits(number2, numBits)
                
                firstInputs.setValue(bits1)
                secondInputs.setValue(bits2)
                
                adder.evaluate()
                
                trueValue = number1 + number2
                ourValue = convertBitsToNumber(outputs)
                
#                print bits1, bits2, outputs, trueValue, ourValue
            
                totalError += ERROR_PUNISHMENT(trueValue, ourValue)
                
                
                
    averageError = totalError / float(numIterations)
    
    return (adder.powerConsumption(), averageError)
                   
Ground = Wire()
Power = Wire()
Power.setValue(1)        
            
def oneBitAdder(inputs, outputs, noise=STANDARD_NOISE()):
    assert len(inputs) == 3
    assert len(outputs) == 2
    return Circuit(inputs, outputs, tuple([Xor3(inputs, outputs[0], noise), Maj3(inputs, outputs[1], noise)]))

# Takes as input two n-bit numbers and returns a (n+1)-bit number    
def nBitAdder(numBits, inputs, outputs, noiseFunction):
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
            [output, carryOut], noiseFunction(i)))
            
        carryIn = carryOut
        
    return Circuit(inputs, outputs, listOfLittleAdders)        

p.xlabel("Power consumption")
p.ylabel("Mean squared error")

for i in range(1,11):
        
    scaling_const = 0.001*i
        
    flatNoise = lambda x : 2*scaling_const
    linearNoise = lambda x : scaling_const*(x+1) 
    expNoise = lambda x : scaling_const * 2**x      
    
    flat = adderTest(4, 100, flatNoise)
    linear = adderTest(4, 100, linearNoise)
    exp = adderTest(4, 100, expNoise)
    
    p.plot(flat[0], flat[1], "bo")
    p.plot(linear[0], linear[1], "ro")
    p.plot(exp[0], exp[1], "go")

p.savefig("adder_error.png")
#b = Bus(4)

#b.setValue((0,1,1,0))

#print b[2]
#print b[1:3] 
 
#print convertBitsToNumber(b) 
        
#firstInputs = Bus(4)
#secondInputs = Bus(4)
#
#inputs = firstInputs.merge(secondInputs)
#outputs = Bus(5)
#                                            
#adder = nBitAdder(4, inputs, outputs)
#
#firstInputs.setValue((0,1,1,0))
#secondInputs.setValue((1,1,0,1))
#
#adder.evaluate()
#
#print adder.countGates()
#print adder.powerConsumption()
#
#print convertNumberToBits(5, 3)
#print convertBitsToNumber((1,1,0))
#
#print outputs