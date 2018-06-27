/**
 * SAP-1 whole system integration
 */
`include "program_counter/program_counter.v"
`include "memory_address_register/memory_address_register.v"
`include "mux_2x4/mux_2x4.v"
`include "ram_16x8/ram_16x8.v"
`include "instruction_register/instruction_register.v"
`include "register/register.v"
`include "alu/alu.v"
`include "controller/controller.v"

module sap
  (
   input        i_clock,
   input        i_reset,
   input        i_program_mode, //0=Execution Mode 1=Program Mode
   input [3:0]  i_program_address, //The address to program
   input [7:0]  i_program_data, //The data to program
   input        i_program_write, //Program commit!
   // Debug flags per unit
   input        i_debug_pc,
   input        i_debug_mar,
   input        i_debug_ram,
   input        i_debug_ir,
   input        i_debug_register_A,
   input        i_debug_register_B,
   input        i_debug_alu,
   input        i_debug_bus,
   input        i_debug_control,
   input        i_debug_out,
   //Output Register - light up seven segment or whatever
   output [7:0] o_display 
   );

   // Control-Sequencer output signals
   wire         ctl_halt;
   wire         ctl_memory_address_in;
   wire         ctl_ram_in;
   wire         ctl_ram_out;
   wire         ctl_instruction_out;
   wire         ctl_instruction_in;
   wire         ctl_register_A_in;
   wire         ctl_register_A_out;   
   wire         ctl_alu_out;
   wire         ctl_alu_subtract;
   wire         ctl_register_B_in;
   wire         ctl_register_output_in;
   wire         ctl_program_counter_increment;
   wire         ctl_program_counter_out;
   wire         ctl_program_counter_jump;   
   
   // Component wires
   wire [7:0]   bus; // Main system bus
   wire [3:0]   mar_address; //Connects to 2 input Mux
   wire [3:0]   ram_address; //Connects from mux into RAM
   wire [3:0]   opcode; //Connects from IR to Controller
   wire [7:0]   alu_A_in; //Connects from Register A to ALU
   wire [7:0]   alu_B_in; //Connects from Register B to ALU
   wire         alu_flag_zero; //Zero result flag from ALU to Controller
   wire         alu_flag_overflow; //Overflow result flag from ALU to Controller

   // RAM should respond to control signals and program mode:
   wire         ram_write = ctl_ram_in || i_program_write;
   wire         ram_clock = i_clock || i_program_write;
   
   program_counter pc 
     (
      .i_debug(i_debug_pc),
      .i_reset(i_reset),
      .i_increment(ctl_program_counter_increment),
      .i_enable_out(ctl_program_counter_out),
      .o_count(bus)
      );

   memory_address_register mar
     (
      .i_debug(i_debug_mar),
      .i_reset(i_reset),
      .i_enable_in(ctl_memory_address_in),
      .i_address(bus[3:0]),
      .o_address(mar_address)
      );

   mux_2x4 mar_mux
     (
      .i_address_1(mar_address),
      .i_address_2(i_program_address),
      .i_input_select(i_program_mode),
      .o_address(ram_address)
      );

   ram_16x8 ram
     (
      .i_debug(i_debug_ram),
      .i_program_mode(i_program_mode),
      .i_program_data(i_program_data),
      .i_address(ram_address),
      .i_write_enable(ram_write),
      .i_read_enable(ctl_ram_out),
      .io_data(bus)
      );
   
   instruction_register ir
     (
      .i_debug(i_debug_ir),
      .i_reset(i_reset),
      .i_load_instruction(ctl_instruction_in),
      .i_send_address(ctl_instruction_out),
      .i_bus(bus),
      .o_opcode(opcode),
      .o_address(bus[3:0])
      );

   register register_A
     (
      .i_debug(i_debug_register_A),
      .i_reset(i_reset),
      .i_load_data(ctl_register_A_in),
      .i_send_data(ctl_register_A_out),
      .i_bus(bus),
      .o_bus(bus),
      .o_unbuffered(alu_A_in)
      );

   register register_B
     (
      .i_debug(i_debug_register_B),
      .i_reset(i_reset),
      .i_load_data(ctl_register_B_in),
      .i_bus(bus),
      .o_bus(), // Register B only outputs unbuffered, to the ALU.
      .o_unbuffered(alu_B_in)
      );

   alu alu
     (
      .i_a(alu_A_in),
      .i_b(alu_B_in),
      .i_subtract(ctl_alu_subtract),
      .i_send_result(ctl_alu_out),
      .o_flag_overflow(alu_flag_overflow),
      .o_flag_zero(alu_flag_zero),
      .o_bus(bus)
      );

   register register_OUT
     (
      .i_debug(i_debug_out),
      .i_reset(i_reset),
      .i_load_data(ctl_register_output_in),
      .i_bus(bus),
      .o_bus(), // Register OUT displays unbuffered data to the display
      .o_unbuffered(o_display)
      );

   controller control
     (
      .i_debug(i_debug_control),
      .i_clock(i_clock),
      .i_reset(i_reset),
      .i_opcode(opcode),
      .i_flag_overflow(alu_flag_overflow),
      .i_flag_zero(alu_flag_zero),
      .o_halt(ctl_halt),
      .o_memory_address_in(ctl_memory_address_in),
      .o_ram_in(ctl_ram_in),
      .o_ram_out(ctl_ram_out),
      .o_instruction_in(ctl_instruction_in),
      .o_instruction_out(ctl_instruction_out),
      .o_register_a_in(ctl_register_A_in),
      .o_register_a_out(ctl_register_A_out),
      .o_alu_out(ctl_alu_out),
      .o_alu_subtract(ctl_alu_subtract),
      .o_register_b_in(ctl_register_B_in),
      .o_register_output_in(ctl_register_output_in),
      .o_program_counter_increment(ctl_program_counter_increment),
      .o_program_counter_out(ctl_program_counter_out),
      .o_program_counter_jump(ctl_program_counter_jump)
      );

   always @(posedge i_reset) begin
      $display("INFO: System Reset");
   end
   
   always @(bus) begin
      if(i_debug_bus) begin
         $display("DEBUG: Bus value now : %b", bus);
      end
   end
   
endmodule // sap
