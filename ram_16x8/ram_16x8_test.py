import cocotb
import numbers
import random
from lib.util import assertions
from lib.cycle import clock, wait, cycle, reset

@cocotb.test()
def ram_16x8(dut):

    def assert_io_data(value, error_msg):
        """Check the value of the data lines"""
        if (isinstance(value, numbers.Number)):
            assertions.assertEqual(dut.io_data.value, value, error_msg)
        else:
            assertions.assertEqual(dut.io_data.value.binstr, value, error_msg)

    def reset_input():
        dut.i_debug = 1
        dut.i_program_mode = 0
        dut.i_program_data.value.binstr = 'zzzzzzzz'
        dut.i_address.value.binstr = 'zzzz'
        dut.i_write_enable = 0
        dut.i_read_enable = 0        
        dut.io_data.value.binstr = 'zzzzzzzz'

        yield from wait()

    def assert_read(address, value, error_msg='wrong data read'):
        dut.i_address = address
        dut.i_read_enable = 1
        yield from wait()
        assert_io_data(value, error_msg)
        dut.i_read_enable = 0
        yield from wait()

    def write_data(address, data):
        dut.i_address = address
        dut.io_data = data
        yield from cycle(dut, 1, ['i_write_enable'])

    def program_data(address, data):
        dut.i_program_mode = 1
        dut.i_address = address
        dut.i_program_data = data
        yield from cycle(dut, 1, ['i_write_enable'])
        dut.i_program_mode = 0
        yield from wait()

    def assert_write(address, data, error_msg='Could not verify written data'):
        yield from write_data(address, data)
        yield from assert_read(address, data, error_msg)
        
    # Initialize
    yield from reset_input()
    yield from wait()
    assert_io_data('zzzzzzzz', 'No output should be made on initialization')

    # Verify all RAM is cleared
    yield from reset_input()
    for addr in range(16):
        assert_read(addr, '00000000', 'RAM address is cleared')
    
    # Manually enter new RAM data
    yield from reset_input()
    data = [random.randint(0,255) for x in range(16)]
    for addr in range(16):
        yield from program_data(addr, data[addr])
    assert_io_data('zzzzzzzz', 'No output should be available unless read is enabled')

    # Read from RAM
    yield from reset_input()
    for addr in range(16):
        assert_read(addr, data[addr])
    
    # Write data from the io_data bus
    yield from reset_input()
    yield from assert_write(0b0010, 0b11001100)

