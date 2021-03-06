import cocotb
from lib.util import assertions
from lib.cycle import clock, wait, reset

@cocotb.test()
def program_counter(dut):

    def assert_o_count(value, error_msg):
        """Check the value of the output count"""
        assertions.assertEqual(dut.o_count.value.binstr, value, error_msg)
        
    # Test initialization
    yield from wait()
    assert_o_count('xxxx', 'o_count should start disconnected')

    # Pulse the clock, nothing should change:
    yield from clock(dut)
    assert_o_count('xxxx', 'o_count should still be disconnected')

    # Enable the output:
    dut.i_enable_out = 1
    yield from wait()
    assert_o_count('0000', 'o_count should be enabled and initialized')

    # Increment:
    dut.i_increment = 1
    yield from wait()
    assert_o_count('0000', 'o_count should not increment until clock pulse')
    yield from clock(dut)
    assert_o_count('0001', 'o_count should increment')
    yield from clock(dut)
    assert_o_count('0010', 'o_count should increment')
    yield from clock(dut)
    assert_o_count('0011', 'o_count should increment')

    # Cycle without increment:
    dut.i_increment = 0
    yield from clock(dut)
    assert_o_count('0011', 'o_count should not increment')

    # Disable and Re-enable output:
    dut.i_enable_out = 0
    yield from wait()
    assert_o_count('zzzz', 'o_count should disconnect')
    dut.i_enable_out = 1
    yield from wait()
    assert_o_count('0011', 'o_count should re-enable')
    
    # Reset:
    yield from reset(dut)
    assert_o_count('0000', 'o_count should reset')

    # Test roll-over:
    dut.i_increment = 1
    # Increment over 8 cycles:
    yield from clock(dut, 8)
    assert_o_count('1000', 'o_count should be 8')
    # Increment over 9 cycles, rolling over the count:
    yield from clock(dut, 9)
    assert_o_count('0001', 'o_count should roll-over back to 1')
