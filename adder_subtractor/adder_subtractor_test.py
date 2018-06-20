import cocotb
from lib.util import assertions
from lib.cycle import clock, wait, reset

@cocotb.test()
def adder_subtractor_test(dut):

    def assert_o_bus(value, error_msg='wrong data'):
        """Check the bus out value"""
        assertions.assertEqual(dut.o_bus.value.binstr, value, error_msg)

    def reset_input():
        dut.i_a = 0
        dut.i_b = 0
        dut.i_subtract = 0
        dut.i_send_result = 0
        yield from wait()


    ### Test init
    yield from reset_input()
    assert_o_bus('zzzzzzzz', 'Output should default disabled')
    

    ### Test add
    dut.i_a = 22
    dut.i_b = 42
    dut.i_send_result = 1
    yield from wait()
    assert_o_bus('01000000', '22 + 42 = 64')


    ### Test subtract
    yield from reset_input()
    dut.i_a = 34
    dut.i_b = 30
    dut.i_subtract = 1
    dut.i_send_result = 1
    yield from wait()
    assert_o_bus('00000100', '34 - 30 = 4')

    ### Test negative numbers
    yield from reset_input()
    dut.i_a = 29
    dut.i_b = 56
    dut.i_subtract = 1
    dut.i_send_result = 1
    yield from wait()    
    assert_o_bus('11100101', '29 - 56 = -27')

    ### Test disconnection from bus
    dut.i_send_result = 0
    yield from wait()
    assert_o_bus('zzzzzzzz', 'Should disconnect from bus')
