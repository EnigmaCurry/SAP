/**
 * 4 bit program counter - PC
 */
module program_counter
  (
   // System clock signal:
   input        i_clock,
   // Count is reset to 0000 when i_reset goes high
   input        i_reset,
   // Count is incremented once per clock cycle if i_increment is high
   input        i_increment,
   // Module output is tri-state; only enabled when i_enable_out is high
   input        i_enable_out,
   // 4 bit count output
   output [3:0] o_count
   );

   // Internal count register
   reg [3:0]    count = 4'b0000;

   // The output is normally disconnected, 
   // only showing the count when i_enable_out goes high:
   assign o_count = i_enable_out ? count : 4'bzzzz;

   // Recalculate count on every clock cycle:
   always @(posedge i_clock or posedge i_reset) begin
      if(i_reset) 
        count <= 4'b0000;
      else if(i_increment)
        count <= (count == 4'b1111) ? 4'b0000 : count + 1'b1;
   end
   
endmodule // program_counter
