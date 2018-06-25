# Simple As Possible Computer (SAP)

_WORK IN PROGRESS_

This project implements a loose interpretation of [Malvino and Brown's
SAP-1 computer
architecture](http://deeprajbhujel.blogspot.com/2015/12/sap-1-architecture.html)
(as first described in [Digital Computer Electronics
(1977)](https://books.google.com/books/about/Digital_Computer_Electronics.html?id=mUWN0aIIqzkC)).
The end goal is to replicate [Ben Eater's TTL
Computer](https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU).
Ben made a fascinating series of Youtube videos where he builds and
extends the SAP-1 architecture, using nothing but simple 74xx
transistors, on breadboard. For my CPU, instead of hand wiring logic
chips, the entire design is defined in software, as Verilog code. This
code can be simulated on a workstation, and proven to operate the way
it is intended. Eventually, this software could be turned into real
hardware on an FPGA board.

This code runs with the [Icarus Verilog](http://iverilog.icarus.com/)
open source simulation tool on a regular Linux PC. Each component of
the system is written and tested in isolation. Each unit is its own
separate directory, with its own Makefile to run a Python test suite,
written with [cocotb](https://github.com/potentialventures/cocotb).
Adhering to this structure means that every unit is fully modular, and
easier to comprehend and test, by drawing a box around it.

Synthesis is not yet supported. I don't own an FPGA development board
yet, but I plan to check out
[IceStorm](http://www.clifford.at/icestorm/), a fully open source
toolchain, once I do. (I hope I haven't written any non-synthesizable
verilog yet! FPGAs only work with a _subset_ of the Verilog language.)
:/

This same project has been implemented several times, in different
ways, by many people:
 * [JetStarBlues/BenEater_CPU](https://github.com/JetStarBlues/BenEater_CPU)
 * [LuisMichaelis/Computer-Simulation](https://github.com/LuisMichaelis/Computer-Simulation)
 * [ellisgl/sap-1-v2-mojo](https://github.com/ellisgl/sap-1-v2-mojo)
 * [Vdragon/SAP_1](https://github.com/Vdragon/Vdragon_s_Verilog_modules/tree/master/SAP_1)
 * [joshcorbin/sap-1-complete](http://joshcorbin.com/sap-1-complete/)
 
Writing your own version of SAP-1, from scratch, is a worthwhile
project. It can be a very elucidating process, whether it materializes
as physical logic chips, on a breadboard, as Hardware Description
Language, running in a virtual machine... or in any abstraction, not
yet realized. (Could reality itself be composed of sucessive lambda
calculus expressions? [a(b)=1; a(1)=a(a(b))=2;
a(6)=a(a(a(a(a(a(b))))))=7; find b;]) Actually going down the path,
and doing the work yourself, shows you what you did not know before:
there is an understanding of how a thing works, and there is a
knowledge of how a thing works. These are not the same thing.

## The SAP-1

SAP-1 is a simple 8-bit computer architecture with only 128 _bits_ of
memory (16 bytes!), 2 program registers, and 5 instructions. A
*really* simple computer. Here's a comparison with a few other 8 bit
computers:

| CPU                                                                                    | Year | Address Size | Max Ram | # registers | # instructions | # transistors |
|----------------------------------------------------------------------------------------|------|--------------|---------|-------------|----------------|---------------|
| SAP-1 (Malvino)                                                                        | 1977 | 4 bits       | 16 B    | 2           | 5              | <500          |
| [Intel 8008](https://en.wikipedia.org/wiki/Intel_8008) (the 'first' 8bit CPU)          | 1972 | 14 bits      | 16 KB   | 7           | 48             | 3500          |
| Apple II ([MOS 6502](https://en.wikipedia.org/wiki/MOS_Technology_6502), Commodore 64) | 1975 | 16 bits      | 64 KB   | 3           | 56             | 4237          |
| TRS-80 ([Z80](https://en.wikipedia.org/wiki/Zilog_Z80))                                | 1977 | 16 bits      | 64 KB   | 17          | 158            | 8500          |


## Architecture

Here is a nice [ASCII diagram from
jk-quantized](https://github.com/JetStarBlues/BenEater_CPU/blob/master/Notes/benEater_cpu):

```
                                ||            --------
                                ||   loNib   |        | <- CO
                                || <-------> |   PC   | <- J
                                ||           |        | <- CE
                                ||            --------
                                ||
                                ||
                                ||
            --------            ||            --------
     MI -> |        |   loNib   ||           |        | <- AI
           |  MAR   | <-------- || <-------> |   A    | <- AO
           |        |           ||           |        |
            --------            ||            --------
               |                ||               |
               | loNib          ||               |
               v                ||               v
            --------            ||            --------
     RI -> |        |           ||           |        | <- ΣO
     R0 -> |  RAM   | <-------> || <-------> |  ALU   | <- SU
           |        |           ||           |        | -> FC
            --------            ||            --------  -> FZ
                                ||               ^
                                ||               |
                                ||               |
            --------            ||            --------
     II -> |        | <-------- ||           |        | <- BI
     IO -> |   IR   |           || --------> |   B    | // <- BO
           |        | --------> ||           |        |
            --------    loNib   ||            --------
               |                ||
               | hiNib          ||
               v                ||
          INSTR DECODER         ||            --------
          AND  CONTROL          ||           |        | <- OI
           SEQUENCER            || --------> |  OUT   |
                                ||           |        |
            --------            ||            --------
     FI -> |        |           ||                |
     FZ -> |   FR   |           ||                |
     FC -> |        |           ||                v
            --------            ||             DISPLAY
                |               ||
                |               ||
                v               ||
              FLAGS             ||
                                ||
```


The two straight lines, going down the middle, represent a shared bus
between components, which is 8 bits wide. The bus can transmit
arbitrary binary data, as well as program instructions. In many other
CPU designs, there are two busses: one for instructions/addresses, and
a separate one for data. The two bus architecture is often called
Harvard design. The SPA-1 design is supposed to be simpler, so both
data, and instructions, share a single bus, like a time-share.

When the bus is used for binary data, all 8 bits of the bus are used.
It's just data. 

When the bus is used for instructions, the 8 bits are split in half:
using the first/left 4 bits (called hiNib) as the Op Code (the 'what'
to do), and the second/right 4 bits (called loNib) as the Operand,
which usually specifies a memory address (the 'thing' to do 'what'
upon).

| Component | Name                     | Size / Type                                                    | Purpose                                                                                                                                        |
|-----------|--------------------------|----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| PC        | Program Counter          | 4 bit counting register (loNib)                                | Counts from 0000->1111 (or until HLT), the pointer to the current instruction in memory.                                                       |
| MAR       | Memory Address Register  | 4 bit register (loNib)                                         | Stores the memory address to actively index in the RAM.                                                                                        |
| RAM       | Memory                   | 16 8bit memory cells (full bus width)                          | 16 bytes of addressable memory: 16 entries, 8 bits each, I/O lines for all 8 bits to/from the bus.                                             |
| IR        | Instruction Register     | 4 bit opcode register (hiNib) / 4 bit address register (loNib) | Stores the current instruction of execution, separates hiNib and loNib, from the bus.                                                          |
| A         | Accumulator (Register A) | 8 bit register (full bus width)                                | Stores the result of computations.                                                                                                             |
| B         | Register B               | 8 bit register (full bus width)                                | Stores the 'other number' for math operations, the number _to_ add/subtract with register A.                                                   |
| ALU       | Arithemetic Logic Unit   | 8 bit adder                                                    | Takes values from register A and B, and performs either add/subtract function, and then puts the result back in A.                             |
| OUT       | Output                   | 8 bit register (full bus width)                                | Stores a snapshot of register A, then shows it to the user.                                                                                    |
| FR        | Flags Register           | 2 bit register flags                                           | Flags are stored when an ADD or SUB instruction results in either: 0 (zero flag) or a number that cannot be represented in 8 bits (carry flag) |

The other symbols on the diagram with arrows pointing in or out of the
units, are the control signals coming from the main Control Sequencer,
discussed later.

## Instruction set

The original SAP-1 has only 5 instructions:

| Instruction | Op code (hiNib) | Operand (loNib)                  | Description                                                    |
|-------------|-----------------|----------------------------------|----------------------------------------------------------------|
| LDA         | 0000            | 4 bit memory address to load     | Load memory at the given address into the accumulator register |
| ADD         | 0001            | 4 bit memory address to add      | Add memory at the given address to the accumulator register    |
| SUB         | 0010            | 4 bit memory address to subtract | Subtract memory at address from accumulator register           |
| OUT         | 1110            | None                             | Send accumulator contents to the output register               |
| HLT         | 1111            | None                             | Halt program                                                   |

The computer is deterministically controlled by the contents of its
RAM. If the RAM contents is changed, then the process of the computer
is changed. Conversely, if the same RAM contents are used multiple
times, the same process is performed every time. Therefore, if you
want the computer to do something, you program the RAM, and the
computer will do what is in the RAM.

The user of SAP-1 is expected to program the RAM before the computer
starts execution. The machine has two modes: program mode, and
execution mode. In program mode, the RAM is disconnected from the bus,
and the user can directly edit the contents of the RAM through input
switches. Both program and data must be input. In execution mode,
these switches are disconnected, and the RAM is connected to the main
bus instead. The RAM provides the program and data for the rest of the
computer to follow and use.

## Example program execution

Here is an example snapshot of the contents of the RAM. The program
containing the instructions always starts at memory address 0000, and
continues until an HLT instruction is found. In this example, the
program is in memory locations 0000 through 0101. Addresses after HLT
is where data storage starts, locations 0110 through 1111, and can
contain data to be used during the execution of the program, using any
of the LDA, ADD, or SUB instructions.

| Memory Address | Memory Contents (hiNib loNib) | Decoded Instruction | Description                                                                                                    |
|----------------|-------------------------------|---------------------|----------------------------------------------------------------------------------------------------------------|
| 0 - 0000       | 0000 1001                     | LDA 9               | Read the contents of memory address 9 (1001) and place the value in register A (16).                           |
| 1 - 0001       | 0001 1110                     | ADD E               | Read the contents of memory address E (1110) and add it to whats already in register A (16 + 127 = 143).       |
| 2 - 0010       | 0010 1101                     | SUB D               | Read the contents of memory address D (1101) and subtract it from whats already in register A (143 - 64 = 79). |
| 3 - 0011       | 1110 xxxx                     | OUT                 | Read the contents of register A, and write it to the output buffer (LEDs, stdout) (Answer shown: 79)           |
| 4 - 0100       | 0001 1010                     | ADD A               | Read the contents of memory address A (1010) and add it to whats already in register A (79 + (-86) = -7).      |
| 5 - 0101       | 1111 xxxx                     | HLT                 | End of Program. Everything after this address is data storage. (Answer still shows 79, because of no 2nd OUT)  |
| 6 - 0110       | xxxx xxxx                     | data                | unused                                                                                                         |
| 7 - 0111       | xxxx xxxx                     | data                | unused                                                                                                         |
| 8 - 1000       | xxxx xxxx                     | data                | unused                                                                                                         |
| 9 - 1001       | 0001 0000                     | data                | The number 16 (programmed in before execution)                                                                 |
| A - 1010       | 1010 1010                     | data                | The number -86 (programmed in before execution)                                                                |
| B - 1011       | xxxx xxxx                     | data                | unused                                                                                                         |
| C - 1100       | xxxx xxxx                     | data                | unused                                                                                                         |
| D - 1101       | 0100 0000                     | data                | The number 64 (programmed in before execution)                                                                 |
| E - 1110       | 0111 1111                     | data                | The number 127 (programmed in before execution)                                                                |
| F - 1111       | xxxx xxxx                     | data                | unused                                                                                                         |

Once the user has programmed all of this data into RAM, the computer
is switched to execution mode. The Program Counter (PC) counts from
0000 to 1111 (or until HLT), which advances through all the memory
addresses, one by one. Starting at memory address 0000, the first
instruction is read, and then executed (LDA 9). The Program Counter
advances to 0001, and the second memory address is read (ADD E), and
then executed, and so on. Once memory address 5 (0101) is read, an HLT
instruction is parsed, and execution stops.

 * The computer program calculates : 16 + 127 - 64
 * Then outputs: 79
 * Then calculates 79 + (-86), but does not display the answer.
 * Then stops.

## Control Sequencer

Since all the components share a single bus, there has to be something
that ensures that only one thing writes to the bus at a time. This
controller should also coordinate when a unit should read from the
bus, and when to ignore it. The letters with arrows, represented in
the diagram, show lines coming from a central controller out to each
of the individual units of the system. The controller fetches an
instruction from RAM, decodes the instruction into the Instruction
Register, and based on this input, the Controller knows what
components to talk to, to carry out the instruction. It has dedicated
wires (not the main bus), running to all the various parts of the
system, and ensures things happen in the right sequence.

These are the control signals output from the main controller:

| Control Signal | Name               | Description                                                                                                                        |
|----------------|--------------------|------------------------------------------------------------------------------------------------------------------------------------|
| HLT            | Halt               | Stops execution of the running program                                                                                             |
| MI             | MAR In             | The Memory Address Register is told to read from the bus                                                                           |
| RI             | RAM In             | The Memory (RAM) is told to read from the bus                                                                                      |
| RO             | RAM Out            | The Memory (RAM) is told to write to the bus                                                                                       |
| IO             | Instruction Out    | The Instruction Register is told to write the address (loNib) to the bus. The opcode (hiNib) is always connected to the Controller |
| II             | Instruction In     | The Instruction Register is told to read from the bus, decode, and store the Instruction                                           |
| AI             | A Register In      | Register A is told to read from the bus and store the data                                                                         |
| AO             | A Register Out     | Register A is told to write to the bus                                                                                             |
| ΣO             | Sum Out            | The ALU is told to write the result of its computation to the bus                                                                  |
| SU             | Subtract           | The ALU is told to do a subtraction operation, rather than addition                                                                |
| BI             | Register B In      | Register B is told to read from the bus and store the data                                                                         |
| OI             | Output Register In | The Output Register is told to read from the bus, store and display the data                                                       |
| CI             | Counter Increment  | The Program Counter is told to increment                                                                                           |
| CO             | Counter Out        | The Program Counter is told to write to the bus                                                                                    |
| J              | Jump               | The Program Counter is told to read from the bus, and update its count to the loNib value                                          |
| FI             | Flags In           | The Flags register is told to store the current ALU flags (connected outside the bus)                                              |

The 'controller' is shorthand for Control Sequencer, as it controls
the process of a single instruction over the duration of several
sequential clock cycles. For the sake of simplicity, the orginal SAP-1
controller defined every instruction as taking 6 clock cycles (or 6
t-states). (Not every instruction needed those 6 cycles, but it is
simpler to implement if you just wait out the extra cycles doing
nothing.) Each t-state of the instruction is carried out sequentially,
with the controller outputing different control signals depending on
the current instruction and step. The controller is programmed for
each instruction and carries out the step-sequence of the control
signals necessary for the given instruction.

For example, examine the LDA instruction. It requires 4 steps (with
each part of a step happening in parallel.)

 1. Do the following Memory Fetch operations, in parallel:
 
     - Tell the Program Counter (PC) to output the current program
       pointer to the main bus. This is the current 'line' of our program,
       (actually it's the address pointing to it, in memory). Any component
       could potentially now read this value from the bus, but it will not
       do so unless the Control Sequencer tells it to.
       
     - The Memory Address Register (MAR) is told to read the main bus.
       For this moment, the MAR and the PC now contain the same value.


 2. Do the following Memory Fetch operations, in parallel:
 
     - Tell the Memory (RAM) to lookup the memory stored for the MAR
       address, and output the data to the main bus. 

     - Tell the Instruction Register (IR) to read from the main bus,
       and to decode and store the current instruction.

     - The Instruction Register is always connected to the Control
       Sequencer, outputting the decoded Opcode from the stored
       instruction (the hiNib, the 'what to do'; LDA in this
       example). This Opcode informs the Control Sequencer in its
       decision for what to do in subsequent steps.

     - Tell the Program Counter (PC) to increment itself, in
       preparation for the next instruction (which won't happen until
       all the steps of the current instruction finish).
 
 3. Do the following LDA specific operations, in parallel:
 
     - Tell the Instruction Register (IR) to output the instruction to
       the bus. The memory address operand of the LDA instruction is
       now on the lower 8 bits (loNib) of the main bus.

     - Tell the Memory Address Register (MAR) to load from the main
       bus. This is the address to load from memory in the next step.

 4. Do the following LDA specific operations, in parallel:
 
     - Tell the Memory (RAM) to lookup the data from the MAR address,
       and output it to the main bus. Now the bus contains the
       contents of memory specified by the LDA instruction.

     - Tell Register A to read from the main bus. Now Register A
       contains the data the LDA instruction told it to load.

The above explanation may seem overly complicated, and expressed in
words, it is. Each step can be simplified if written with
combinatorial logic, using the Control Signal names as labels. Here
are all five of the orignal SAP-1 instructions, each expressed as a
control sequence comprised of 6 t-states (not all used):

| Instruction | T-1    | T-2    | T-3    | T-4    | T-5            | T-6 |
|-------------|--------|--------|--------|--------|----------------|-----|
| LDA         | MI, CO | RO, CI | MI, IO | RO, AI |                |     |
| ADD         | MI, CO | RO, CI | MI, IO | RO, BI | AI, ΣO, FI     |     |
| SUB         | MI, CO | RO, CI | MI, IO | RI, BI | AI, ΣO, SU, FI |     |
| OUT         | MI, CO | RO, CI | AO, OI |        |                |     |
| HLT         | MI, CO | RO, CI | HLT    |        |                |     |

Notice that for all of the instructions, the first two t-states are
identical. T-1 and T-2, combined, are called the Fetch cycle, as it is
the same steps that any instruction will need to perform in order to
load the next instruction from RAM. Steps T-3 through T-6 are specific
to the Instruction type, and are therefore different for each
instruction.

These control sequences are implemented in the hardware design of the
Control Sequencer. This is easy to do in Verilog, because if you want
to modify the architecture, perhaps to add a new type of Instruction,
you just modify the code. In Ben's breadboard design, he implemented
these control sequences as an eeprom. This makes his design flexible,
should he want to add additional instructions (see the next section).
To do so, he does not need to change any of the existing wires, just
reprogram the eeprom. In our Verilog design, the whole implementation
is programmed, so this is an unnecessary complication. We don't need
microcode, we can just hardcode the control sequences directly into
the Control Sequencer implementation, and recompile when changes are
made. (This decision is more conducive to FPGA implementation than
ASIC design. An ASIC that supports microcode is software upgradeable.
A hardcoded ASIC implementation is not.)

## Is this really a computer though?

With only five instructions, the only things SPA-1 can do are: Read
memory; Add and Subtract 8 bit numbers; Show the result; and Stop.
This is a calculator, not a full computer. To make this system useful,
more instructions need to be created. (Up to 16 instructions can be
created, using 4bit op codes.) As Ben shows, in his video [Making a
computer Turing
complete](https://www.youtube.com/watch?v=AqNDk_UJW4k), its only a
handful of additonal instructions that are necessary to make this a
universal Turing Machine <sup>(still only with 16B of memory)</sup>.
Ben uses a modified instruction set (note the opcode changes):

| Instruction | Op code (hiNib) | Operand (loNib)                    | Description                                                                                     |
|-------------|-----------------|------------------------------------|-------------------------------------------------------------------------------------------------|
| NOP         | 0000            | None                               | No operation                                                                                    |
| LDA         | 0001            | 4 bit memory address to read       | Read the contents of the given memory address, store it in the A register.                      |
| ADD         | 0010            | 4 bit memory address to add        | Add the contents of the given memory address to the A register.                                 |
| SUB         | 0011            | 4 bit memory address to subtract   | Subtract the contents of the given memory address from the A register.                          |
| STA         | 0100            | 4 bit memory address to write      | Write the contents of the A register into the memory at the given address.                      |
| LDI         | 0101            | 4 bit number to give to A directly | Load Data Immediately into register A, given the operand number (0-15). No RAM read.            |
| JMP         | 0110            | 4 bit number to give to P. Counter | Jump. Set the Program Counter to the given operand, which will be the next instruction pointer. |
| JC          | 0111            | 4 bit number to give to P. Counter | Jump conditionally, on carry flag.                                                              |
| JZ          | 1000            | 4 bit number to give to P. Counter | Jump conditionally, on zero flag.                                                               |
| OUT         | 1110            | None                               | Send accumulator contents to the output register.                                               |
| HLT         | 1111            | None                               | Halt program.                                                                                   |

The addition of the ability to store data back to RAM, and the three
new jump instructions, provide the capabilities of a Turing Machine; a
computer that is capable of calculating any calculable problem
<sup>(within memory constraints)</sup>.

# Setup for development and simulation

```
# Install dependencies (I use Arch Linux):
pacman -S iverilog

# Clone repository
git clone https://github.com/EnigmaCurry/SAP.git
cd SAP

# Checkout cocotb submodule
git submodule init
git submodule update

# Each component has its own Makefile in its own directory.
# Running 'make' will simulate the component by itself, driven 
# by a Python test bench found in the same directory:
cd program_counter
make

# Integration tests are tests that invole two or more components
# interacting together at the same time. Find these tests in the
# integration/test directory:
cd ../integration/test/pc_and_mar
make

# Eventually there will be a Makefile here in the root directory that
# wraps all the components together to form a single CPU module. For
# now, this is all just a bunch of individual parts.
```

