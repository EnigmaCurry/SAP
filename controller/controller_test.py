import cocotb
import numbers
from lib.util import assertions
from lib.cycle import clock, wait, reset

@cocotb.test()
def controller_test(dut):
    
    def assert_control(control_bits, error_msg='wrong bits'):
        """Check the control bits output"""
        # Reverse the order of the bits, so they have the same index as in verilog:
        control_bits = control_bits[::-1]
        # Remove blanks used for debug delimiter:
        control_bits = control_bits.replace('_','')
        # Check it:
        assertions.assertEqual(dut.o_halt.value.binstr, control_bits[15], 'incorrect halt value')
        assertions.assertEqual(dut.o_memory_address_in.value.binstr, control_bits[14], 'incorrect MAR In')
        assertions.assertEqual(dut.o_ram_in.value.binstr, control_bits[13], 'incorrect RAM In')
        assertions.assertEqual(dut.o_ram_out.value.binstr, control_bits[12], 'incorrect RAM Out')
        assertions.assertEqual(dut.o_instruction_in.value.binstr, control_bits[11], 'incorrect Instruction In')
        assertions.assertEqual(dut.o_instruction_out.value.binstr, control_bits[10], 'incorrect Instruction Out')
        assertions.assertEqual(dut.o_register_a_in.value.binstr, control_bits[9], 'incorrect Register A In')
        assertions.assertEqual(dut.o_register_a_out.value.binstr, control_bits[8], 'incorrect Register A Out')
        assertions.assertEqual(dut.o_alu_out.value.binstr, control_bits[7], 'incorrect ALU Out')
        assertions.assertEqual(dut.o_alu_subtract.value.binstr, control_bits[6], 'incorrect ALU Subtract')
        assertions.assertEqual(dut.o_register_b_in.value.binstr, control_bits[5], 'incorrect Register B In')
        assertions.assertEqual(dut.o_register_output_in.value.binstr, control_bits[4], 'incorrect Register Out In')
        assertions.assertEqual(dut.o_program_counter_increment.value.binstr, control_bits[3], 'incorrect PC Increment')
        assertions.assertEqual(dut.o_program_counter_out.value.binstr, control_bits[2], 'incorrect PC Out')
        assertions.assertEqual(dut.o_program_counter_jump.value.binstr, control_bits[1], 'incorrect PC Jump')
        assertions.assertEqual(dut.o_register_flags_in.value.binstr, control_bits[0], 'incorrect Register Flags In')

    def assert_step(value, error_msg='wrong assumed step count'):
        if isinstance(value, numbers.Number):
            value = format(value, '03b')
        assertions.assertEqual(dut.o_step.value.binstr, value, error_msg)
        
    def reset():
        dut.i_opcode = 0b0000
        dut.i_flag_carry = 0
        dut.i_flag_zero = 0
        dut.i_reset = 1
        yield from wait()
        dut.i_reset = 0
        assert_step(0)

    def assert_fetch_cycle():
        assert_step(0, 'fetch cycle should start at step 0')
        yield from clock(dut)
        assert_control('0100_0000_0000_0100', 'Fetch step 0')
        
        assert_step(1, 'fetch cycle step 1')
        yield from clock(dut)
        assert_control('0001_0100_0000_1000', 'Fetch step 1')

        assert_step(2, 'Next: Instruction cycle 1 step 2')
        yield from clock(dut)
        
    ### Test Init
    yield from reset()
    assert_control('0000_0000_0000_0000','NOP Init')

    ### Test NOP
    yield from assert_fetch_cycle()
    assert_control('0000_0000_0000_0000','NOP cycle 1')
    
    ### Test LDA
    dut.i_opcode = 0b0001
    yield from assert_fetch_cycle()
    assert_control('0100_1000_0000_0000', 'LDA cycle 1 - MI | IO')
    yield from clock(dut)
    assert_control('0001_0010_0000_0000', 'LDA cycle 2 - RO | AI')

    ### Test ADD
    dut.i_opcode = 0b0010
    yield from assert_fetch_cycle()
    assert_control('0100_1000_0000_0000', 'ADD cycle 1 - MI | IO')
    yield from clock(dut)
    assert_control('0001_0000_0010_0000', 'ADD cycle 2 - RO | BI')
    yield from clock(dut)
    assert_control('0000_0010_1000_0001', 'ADD cycle 3 - AI | EO | FI')

    ### Test SUB
    dut.i_opcode = 0b0011
    yield from assert_fetch_cycle()
    assert_control('0100_1000_0000_0000', 'SUB cycle 1 - MI | IO')
    yield from clock(dut)
    assert_control('0001_0000_0010_0000', 'SUB cycle 2 - RO | BI')
    yield from clock(dut)
    assert_control('0000_0010_1100_0001', 'SUB cycle 3 - AI | EO | SU | FI')

    ### Test STA
    dut.i_opcode = 0b0100
    yield from assert_fetch_cycle()
    assert_control('0100_1000_0000_0000','STA cycle 1 - MI | IO |')
    yield from clock(dut)
    assert_control('0010_0001_0000_0000','STA cycle 2 - RI | AO ')

    ### Test LDI
    dut.i_opcode = 0b0101
    yield from assert_fetch_cycle()
    assert_control('0000_1010_0000_0000','LDI cycle 1 - IO | AI')

    ### Test JMP
    dut.i_opcode = 0b0110
    yield from assert_fetch_cycle()
    assert_control('0000_1000_0000_0010','JMP cycle 1 - IO | J')

    ### Test JC without carry
    dut.i_opcode = 0b0111
    dut.i_flag_carry = 0
    yield from assert_fetch_cycle()
    assert_control('0000_0000_0000_0000', 'JC cycle 1 (without carry): NOP')

    ### Test JC with carry
    dut.i_opcode = 0b0111
    dut.i_flag_carry = 1
    yield from assert_fetch_cycle()
    assert_control('0000_1000_0000_0010', 'JC cycle 1 (with carry): IO | J')

    ### Test JZ without zero result
    dut.i_opcode = 0b1000
    dut.i_flag_zero = 0
    yield from assert_fetch_cycle()
    assert_control('0000_0000_0000_0000', 'JZ cycle 1 (without zero result): NOP')

    ### Test JZ with zero result
    dut.i_opcode = 0b1000
    dut.i_flag_zero = 1
    yield from assert_fetch_cycle()
    assert_control('0000_1000_0000_0010', 'JZ cycle 1 (with zero result): IO | J')

    ### Test OUT
    dut.i_opcode = 0b1110
    yield from assert_fetch_cycle()
    assert_control('0000_0001_0001_0000','OUT cycle 1 - AO | OI')

    ### Test HLT
    dut.i_opcode = 0b1111
    yield from assert_fetch_cycle()
    assert_control('1000_0000_0000_0000','HLT cycle 1 - HLT')

    
