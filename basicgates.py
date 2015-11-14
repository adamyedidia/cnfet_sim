from noisycomponents import *

def And(inputs, output, noise=STANDARD_NOISE()):        
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):0, (0,1):0, (1,0):0, (1,1):1})

def Or(inputs, output, noise=STANDARD_NOISE()):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):0, (0,1):1, (1,0):1, (1,1):1})
    
def Nand(inputs, output, noise=STANDARD_NOISE()):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):1, (0,1):1, (1,0):1, (1,1):0})
    
def Nor(inputs, output, noise=STANDARD_NOISE()):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):1, (0,1):0, (1,0):0, (1,1):0})   
    
def Xor(inputs, output, noise=STANDARD_NOISE()):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):0, (0,1):1, (1,0):1, (1,1):0}, noise)   
    
def Xnor(inputs, output, noise=STANDARD_NOISE()):
    assert len(inputs) == 2
    return LUT(inputs, output, {(0,0):1, (0,1):0, (1,0):0, (1,1):1}, noise)       
    
def Maj3(inputs, output, noise=STANDARD_NOISE()):
    assert len(inputs) == 3
    return LUT(inputs, output, {(0,0,0): 0,
                                (0,0,1): 0,
                                (0,1,0): 0,
                                (0,1,1): 1,
                                (1,0,0): 0,
                                (1,0,1): 1,
                                (1,1,0): 1,
                                (1,1,1): 1}, noise)
                                
def Xor3(inputs, output, noise=STANDARD_NOISE()):
    assert len(inputs) == 3
    return LUT(inputs, output, {(0,0,0): 0,
                                (0,0,1): 1,
                                (0,1,0): 1,
                                (0,1,1): 0,
                                (1,0,0): 1,
                                (1,0,1): 0,
                                (1,1,0): 0,
                                (1,1,1): 1}, noise)
                                