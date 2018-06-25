/** 8 bit 2s complement adder or subtractor
 */

module alu
  (
   input [7:0]  i_a,
   input [7:0]  i_b,
   input        i_subtract, // 0: ADD, 1: SUBTRACT
   input        i_send_result,
   output       o_flag_overflow,
   output       o_flag_zero,
   output [7:0] o_bus
   );

   reg [7:0]    result;
   reg          overflow_flag = 0;
   reg          zero_flag = 0;   
   
   assign o_flag_overflow = overflow_flag;
   assign o_flag_zero = zero_flag;
   assign o_bus = i_send_result ? result : 8'bzzzzzzzz;
   
   always @(posedge i_send_result) begin
      // tri-state output:
      result = i_subtract ? (i_a - i_b) : (i_a + i_b);
      
      // Two's complement overflow detection rules:
      //   - If the sum of two positive numbers yields a negative result, the sum has overflowed.
      //   - If the sum of two negative numbers yields a positive result, the sum has overflowed.
      //   - Otherwise, the sum has not overflowed.
      overflow_flag <= ((!i_subtract && !i_a[7] && !i_b[7] && result[7]) || 
                        (!i_subtract && i_a[7] && i_b[7] && !result[7]) ||
                        (i_subtract && !i_a[7] && i_b[7] && !result[7]) ||
                        (i_subtract && i_a[7] && !i_b[7] && result[7])) ? 1 : 0;

      zero_flag <= (result == 8'b00000000) ? 1 : 0;
   end
   
endmodule // adder_subtractor

