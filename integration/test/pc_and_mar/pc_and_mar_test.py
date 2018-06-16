import cocotb
from util import assertions, cycle, wait

@cocotb.test()
def pc_and_mar(dut):

    def assert_o_address(value, error_msg):
        """Check the value of the output address"""
        assertions.assertEqual(dut.o_address.value.binstr, value, error_msg)

    dut.i_enable = 1
    yield from cycle(dut, 4, ('i_clock','i_increment'))
    # MAR is one cycle behind PC, so after 4 cycles, MAR should contain 3
    assert_o_address('0011', 'When PC has counted to 4, MAR should contain 3.')
