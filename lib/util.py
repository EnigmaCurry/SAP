from cocotb.triggers import Timer

# Use unittest just for its assertion library:
import unittest
assertions = unittest.TestCase('__init__')

def wait():
    """Wait for the simulation, without cycling the clock"""
    yield Timer(1)
        
def cycle(dut, n=1, inputs=('i_clock',)):
    """Cycle n times"""
    for x in range(n):
        for i in inputs:
            setattr(dut, i, 1)
        yield from wait()
        for i in inputs:
            setattr(dut, i, 0)
        yield from wait()
