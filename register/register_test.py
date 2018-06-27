import cocotb
from lib.util import assertions
from lib.cycle import wait, reset

@cocotb.test()
def register(dut):

    def assert_o_bus(value, error_msg='wrong data'):
        """Check the bus out value"""
        assertions.assertEqual(dut.o_bus.value.binstr, value, error_msg)

    def assert_o_unbuffered(value, error_msg='wrong data'):
        """Check the unbuffered output"""
        assertions.assertEqual(dut.o_unbuffered.value.binstr, value, error_msg)

    def reset_input():
        dut.i_bus = 0
        dut.i_load_data = 0
        dut.i_send_data = 0
        dut.i_reset = 0
        yield from wait()

    #### Test initialization
    yield from reset_input()
    assert_o_bus('zzzzzzzz')

    #### Test loading data
    # Simulate an data on the bus:
    dut.i_bus = 0b01000010
    # Tell the register to load it:
    dut.i_load_data = 1
    yield from wait()
    assert_o_unbuffered('01000010', 'Data should go to unbuffered out immediately')
    yield from reset_input()
    assert_o_bus('zzzzzzzz', 'Data should be latched in, but not output yet.')

    #### Test sending data
    dut.i_send_data = 1
    yield from wait()
    assert_o_bus('01000010', 'Data should be output now')
    assert_o_unbuffered('01000010', 'Data should go to unbuffered still')

    #### Test reset
    yield from reset_input()
    dut.i_reset = 1
    yield from wait()
    assert_o_bus('zzzzzzzz', 'bus output disconnected')
    assert_o_unbuffered('zzzzzzzz', 'unbuffered data is now undefined')
