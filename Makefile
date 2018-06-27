SAP_HOME=$(PWD)
DUT=sap

build:
	make clean
	make all

clean::
	find . -type d | grep /sim_build$ | xargs rm -rf

include $(SAP_HOME)/lib/UnitMakefile
