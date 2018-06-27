import cocotb
from lib.util import assertions
from lib.cycle import clock, cycle, wait, reset

@cocotb.test()
def instruction_register(dut):

    def assert_o_opcode(value, error_msg='wrong opcode'):
        """Check the decoded opcode output"""
        assertions.assertEqual(dut.o_opcode.value.binstr, value, error_msg)

    def assert_o_address(value, error_msg='wrong address'):
        """Check the decoded address output"""
        assertions.assertEqual(dut.o_address.value.binstr, value, error_msg)

    def reset_input():
        dut.i_debug = True
        dut.i_bus.value.binstr = 'zzzzzzzz'
        dut.i_load_instruction = 0
        dut.i_send_address = 0
        dut.i_reset = 0
        yield from wait()

    def assert_load_instruction(instruction):
        opcode, operand = (instruction[:4], instruction[4:])
        yield from reset_input()
        dut.i_bus = int(instruction, 2)
        yield from wait()

        yield from cycle(dut, 1, ['i_load_instruction'])
        assert_o_opcode(opcode,'opcode should be loaded immediately')
        assert_o_address('zzzz','address bus should be silent until i_send_address=1')
        
        dut.i_send_address = 1
        yield from wait()
        assert_o_opcode(opcode,'opcode should still be available')
        assert_o_address(operand,'address should write to the bus')

        yield from reset_input()
        assert_o_opcode(opcode,'opcode should remember even when reset')
        assert_o_address('zzzz','address bus is silent on reset')
        dut.i_send_address = 1
        yield from wait()
        assert_o_opcode(opcode,'opcode should still be available')
        assert_o_address(operand,'address should write to the bus again')

    yield from assert_load_instruction('00011101')
