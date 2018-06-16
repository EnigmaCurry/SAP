COCOTB=$(PWD)/../cocotb
DUT=$(notdir $(patsubst %/,%,$(PWD)))
VERILOG_SOURCES=$(PWD)/$(DUT).v
PYTHONPATH:=../lib:$(PYTHONPATH)
TOPLEVEL := $(DUT)
MODULE   := $(DUT)_test

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim
