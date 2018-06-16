import cocotb
from lib.util import assertions
from lib.cycle import wait, clock

@cocotb.test()
def memory_address_register(dut):

    def assert_o_address(value, error_msg):
        """Check the output address"""
        assertions.assertEqual(dut.o_address.value.binstr, value, error_msg)

    # Test initialization
    yield from wait() 
    assert_o_address('0000', 'Address should initialize to 0000')
    dut.i_reset = 0

    # Set the input address to store
    dut.i_address = 0b0100
    yield from wait()
    assert_o_address('0000', 'Address should not change until enabled')

    # Enable the input
    dut.i_enable_in = 1
    yield from wait()
    assert_o_address('0000', 'Address should not change until next cycle')

    # Pulse the clock, and the output should now be the same as the input
    yield from clock(dut)
    assert_o_address('0100', 'Address should change to 0100')

    # Reset the address
    dut.i_reset = 1
    yield from wait()
    assert_o_address('0000', 'Address should reset to 0000')
    dut.i_reset = 0
    yield from wait()
