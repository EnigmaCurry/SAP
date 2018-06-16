"""
Drivers to cycle common module inputs.
Cycle means setting a value high, waiting, then setting back to low.
"""
from cocotb.triggers import Timer

def wait():
    """Wait for the simulation, without cycling anything."""
    yield Timer(1)
        
def cycle(dut, n=1, signals=('i_clock',)):
    """Cycle a signal n times"""
    for x in range(n):
        for s in signals:
            setattr(dut, s, 1)
        yield from wait()
        for s in signals:
            setattr(dut, s, 0)
        yield from wait()

def clock(dut, n=1):
    """Cycle the i_clock input signal n times"""
    yield from cycle(dut, n, signals=('i_clock',))
        
def reset(dut, n=1):
    """Cycle the i_reset input signal n times"""
    yield from cycle(dut, n, signals=('i_reset',))

