// Combine the Program Counter and the Memory Address Register together
`include "../../../program_counter/program_counter.v"
`include "../../../memory_address_register/memory_address_register.v"

module pc_and_mar
  (
   input        i_clock,
   input        i_reset,
   input        i_increment,
   input        i_enable,
   output [3:0] o_address
   );

   wire [3:0]   pc_count;
   wire [3:0]   mar_address;
   assign o_address = mar_address;
   
   program_counter pc 
     (
      .i_clock(i_clock),
      .i_reset(i_reset),
      .i_increment(i_increment),
      .i_enable_out(i_enable),
      .o_count(pc_count)
      );
   
   memory_address_register mar
     (
      .i_clock(i_clock),
      .i_reset(i_reset),
      .i_enable_in(i_enable),
      .i_address(pc_count),
      .o_address(mar_address)
      );
   
endmodule // pc_and_mar
