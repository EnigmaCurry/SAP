import cocotb
import random
from lib.util import assertions
from lib.cycle import clock, wait, reset

@cocotb.test()
def ram_16x8(dut):

    def assert_io_data(value, error_msg):
        """Check the value of the data lines"""
        assertions.assertEqual(dut.io_data.value.binstr, value, error_msg)

    def reset_input():
        dut.i_program_mode = 0
        dut.i_data_program = 0b00000000
        dut.i_address = 0b0000
        dut.i_write_enable = 0
        dut.i_read_enable = 0        
        dut.io_data = 0b00000000
        yield from wait()

    # Initialize
    yield from reset_input()
    assert_io_data('zzzzzzzz', 'No output should be made on initialization')

    # Verify all RAM is cleared
    yield from reset_input()
    dut.i_read_enable = 1
    for i in range(15):
        dut.i_address = i
        yield from wait()
        assert_io_data('00000000', 'RAM address is cleared')
    
    # Manually enter new RAM data
    data = [random.randint(0,255) for x in range(15)]
    yield from reset_input()
    dut.i_program_mode = 1
    dut.i_write_enable = 1
    for i in range(15):
        dut.i_address = i
        dut.i_data_program = data[i]
        yield from wait()
    assert_io_data('zzzzzzzz', 'No output should be available until read is enabled')

    # Read from RAM
    yield from reset_input()
    dut.i_read_enable = 1
    for i in range(15):
        dut.i_address = i
        yield from wait()
        assert_io_data("{0:b}".format(data[i]).zfill(8),
                       'Data should be the same as we wrote')
    
    # Write data from the io_data bus
    yield from reset_input()
    dut.i_write_enable = 1
    dut.i_address = 0b0010
    dut.io_data = 0b11001100
    yield from wait()

    # Read back the data written from the io_data bus
    yield from reset_input()
    dut.i_read_enable = 1
    dut.i_address = 0b0010
    yield from wait()
    assert_io_data('11001100', 'Data written by the io_data bus should be available')

    
