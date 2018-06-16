from cocotb.triggers import Timer

# Use unittest just for its assertion library:
import unittest
assertions = unittest.TestCase('__init__')

def wait():
    """Wait for the simulation, without cycling the clock"""
    yield Timer(1)
        
def cycle(dut, n=1, input='i_clock'):
    """Cycle n times"""
    for x in range(n):
        setattr(dut, input, 1)
        yield from wait()
        setattr(dut, input, 0)
        yield from wait()
