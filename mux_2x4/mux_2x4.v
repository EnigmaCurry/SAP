/**
 * 2-way 4-bit mux for Memory Addresses
 * Used for switching between the PC/MAR and Manual Input
 */
module mux_2x4
  (
   input [3:0]  i_address_1,
   input [3:0]  i_address_2,
   input        i_input_select,
   output [3:0] o_address
   );

   assign o_address = i_input_select ? i_address_2 : i_address_1;
   
   
endmodule // mux_2x4



