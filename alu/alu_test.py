import cocotb
from lib.util import assertions
from lib.cycle import clock, wait, reset

@cocotb.test()
def alu_test(dut):

    def assert_o_bus(value, error_msg='wrong data'):
        """Check the bus out value"""
        assertions.assertEqual(dut.o_bus.value.binstr, value, error_msg)

    def assert_overflow(overflow=True, error_msg='expected overflow flag did not register'):
        """Ensure that the overflow flag was set (or not)"""
        assertions.assertEqual(dut.o_flag_overflow.value.binstr, '1' if overflow else '0', error_msg)

    def assert_zero(zero=True, error_msg='expected zero flag did not register'):
        """Ensure that the zero flag was set (or not)"""
        assertions.assertEqual(dut.o_flag_zero.value.binstr, '1' if zero else '0', error_msg)

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
    assert_overflow(False)
    assert_zero(False)

    ### Test subtract
    yield from reset_input()
    dut.i_a = 34
    dut.i_b = 30
    dut.i_subtract = 1
    dut.i_send_result = 1
    yield from wait()
    assert_o_bus('00000100', '34 - 30 = 4')
    assert_overflow(False)
    assert_zero(False)

    ### Test negative numbers
    yield from reset_input()
    dut.i_a = 29
    dut.i_b = 56
    dut.i_subtract = 1
    dut.i_send_result = 1
    yield from wait()    
    assert_o_bus('11100101', '29 - 56 = -27')
    assert_overflow(False)
    assert_zero(False)

    ### Test numbers larger than we handle:
    yield from reset_input()
    dut.i_a = 127
    dut.i_b = 127
    dut.i_send_result = 1
    yield from wait()
    assert_o_bus('11111110', '127 + 127 =  -2 with overflow')
    assert_overflow()
    assert_zero(False)
    
    ### Test zero flag:
    yield from reset_input()
    dut.i_a = -2
    dut.i_b = 2
    dut.i_send_result = 1
    yield from wait()
    assert_o_bus('00000000','-2 + 2 = 0')
    assert_zero()
    
    ### Test disconnection from bus
    dut.i_send_result = 0
    yield from wait()
    assert_o_bus('zzzzzzzz', 'Should disconnect from bus')
