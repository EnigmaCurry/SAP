import cocotb
from lib.util import assertions
from lib.cycle import clock, wait, reset

@cocotb.test()
def mux_2x4(dut):

    def assert_o_address(value, error_msg):
        """Check the value of the output address"""
        assertions.assertEqual(dut.o_address.value.binstr, value, error_msg)
        
    dut.i_address_1 = 0b0101
    dut.i_address_2 = 0b1010

    dut.i_input_select = 0
    yield from wait()
    assert_o_address('0101', 'Output address should be first input')

    dut.i_input_select = 1
    yield from wait()
    assert_o_address('1010', 'Output address should be second input')
