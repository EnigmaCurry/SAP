import cocotb
from lib.util import assertions
from lib.cycle import clock, wait, cycle, reset

@cocotb.test()
def sap(dut):

    def assert_o_display(value, error_msg='Unexpected display value'):
        """Check the display out value"""
        assertions.assertEqual(dut.o_display.value.binstr, value, error_msg)

    def reset_input():
        dut.i_program_mode = 0
        dut.i_program_address = 0b0000
        dut.i_program_data = 0b00000000
        dut.i_program_write = 0
        # Each component has a seperate debug line to selectively enable:
        dut.i_debug_pc = True
        dut.i_debug_mar = True
        dut.i_debug_ir = True
        dut.i_debug_ram = True
        dut.i_debug_bus = True
        dut.i_debug_control = True
        dut.i_debug_out = True
        dut.i_debug_register_A = True
        dut.i_debug_register_B = True
        yield from wait()

    def program_ram(address, data):
        dut.i_program_address = address
        dut.i_program_data = data
        yield from cycle(dut, 1, ('i_program_write',))

    def reset():
        yield from reset_input()
        dut.i_reset = 1
        yield from wait()
        dut.i_reset = 0
        yield from wait()

    ### Total system reset:
    yield from reset()

    ### Test program mode:
    dut.i_program_mode = 1
    # LDA 9 (=16)
    yield from program_ram(0b0000,0b00011001)
    # ADD E (16+127=143)
    yield from program_ram(0b0001,0b00101110)
    # SUB D (143-64=79)
    yield from program_ram(0b0010,0b00111101)    
    # OUT (Displays 79)
    yield from program_ram(0b0011,0b11100000)
    # RAM address 9 = 16
    yield from program_ram(0b1001,0b00010000)
    # RAM address E = 127
    yield from program_ram(0b1110,0b01111111)
    # RAM address D = 64
    yield from program_ram(0b1101,0b01000000)
    
    ### Test execution
    yield from reset_input()
    ### Wait for LDA - 4 cycles
    yield from clock(dut, 4)
    ### Wait for ADD - 5 cycles
    yield from clock(dut, 5)
    ### Wait for SUB - 5 cycles
    yield from clock(dut, 5)
    ### Wait for OUT - 3 cycles
    yield from clock(dut, 3)

    
    assert_o_display('01001111', 'Output should be 79')
