import cocotb
from lib.util import assertions
from lib.cycle import clock, wait, reset

@cocotb.test()
def instruction_register(dut):

    def assert_o_opcode(value, error_msg='wrong opcode'):
        """Check the decoded opcode output"""
        assertions.assertEqual(dut.o_opcode.value.binstr, value, error_msg)

    def assert_o_address(value, error_msg='wrong address'):
        """Check the decoded address output"""
        assertions.assertEqual(dut.o_address.value.binstr, value, error_msg)

    def reset_input():
        dut.i_bus = 0b00000000
        dut.i_load_instruction = 0
        dut.i_send_address = 0
        dut.i_reset = 0
        yield from wait()

    #### Test initialization
    yield from reset_input()
    # The opcode is going directly to the control/sequencer, and does not need
    # to be tri-state, so it starts at 0000:
    assert_o_opcode('0000')
    # The address output is connected to the main bus, so it needs to be
    # tri-state. It initializes disconnected:
    assert_o_address('zzzz')

    #### Test loading an instruction
    # Simulate an instruction on the bus:
    dut.i_bus = 0b01000010
    # Tell the register to load it:
    dut.i_load_instruction = 1
    yield from wait()
    assert_o_opcode('0000', 'Instruction should not be read until the next clock cycle') 
    assert_o_address('zzzz', 'Address should not be connected to bus yet')
    # Now tell it to output the address to the bus.
    # It won't output the change until next clock cycle:
    dut.i_send_address = 1
    yield from wait()
    assert_o_opcode('0000', 'Opcode wont change til next clock')
    assert_o_address('0000', 'At this point the address is being output,'
                     ' but the new value wont appear til next clock')
    # Advance the clock, triggering the new address output to the bus:
    yield from clock(dut)
    assert_o_opcode('0100', 'Opcode is ready') 
    assert_o_address('0010', 'New address output to the bus')

    #### Test holding onto the value
    # We can reset all the inputs, and still remember the value :)
    yield from reset_input()
    # Even if we advance the clock now, we still have the values in the register:
    yield from clock(dut, n=5)
    assert_o_opcode('0100', 'Instruction opcode should always output')
    assert_o_address('zzzz', 'Address is not available until i_send_address=1 again')
    # Test sending the same address to the bus again:
    dut.i_send_address = 1
    yield from wait()
    assert_o_address('0010', 'Address is again available on the bus')

    #### Test reset
    yield from reset_input()
    dut.i_reset = 1
    yield from wait()
    assert_o_opcode('0000', 'Op code reset')
    assert_o_address('zzzz','Address reset to tri-state')
