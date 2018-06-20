/** 8 bit 2s complement adder or subtractor
 */

module adder_subtractor
  (
   input [7:0]  i_a,
   input [7:0]  i_b,
   input        i_subtract, // 0: ADD, 1: SUBTRACT
   input        i_send_result,
   output [7:0] o_bus
   );
 
   // tri-state output: disconnected, add, or subtract:
   assign o_bus = i_send_result ? (i_subtract ? (i_a - i_b) : (i_a + i_b)) : 8'bzzzzzzzz;

endmodule // adder_subtractor

