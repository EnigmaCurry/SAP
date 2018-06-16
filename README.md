# Simple As Possible Computer (SAP-1)

_WORK IN PROGRESS_

This project contains Verilog code that implements a loose
interpretation of Malvino's SAP1 computer architecture.

Each component of the system is tested in isolation. Each unit has its
own Makefile and python test suite, written with
[cocotb](https://github.com/potentialventures/cocotb).

## Setup for development and simulation

```
# Install dependencies (I use Arch Linux):
pacman -S iverilog

# Clone repository
git clone https://github.com/EnigmaCurry/SAP1.git
cd SAP1

# Checkout cocotb submodule
git submodule init
git submodule update

# Each component has its own Makefile in its own directory.
# Running 'make' will simulate the chip, driven by the Python test
# bench found in the same directory:
cd program_counter
make
```

## Setup for FPGA synthesis

I don't have one yet :(

