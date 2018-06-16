/**
 * 4 bit memory address register - MAR
 */
module memory_address_register
  (
   // System clock signal:
   input        i_clock,
   // 4 bit address to store
   input [3:0]  i_address,
   // Only allow storing address when enabled
   input        i_enable_in,
   // Reset address to 0000
   input        i_reset,
   // 4 bit address output:
   output [3:0] o_address
   );

   // Internal address register
   reg [3:0]    address = 4'b0000;

   assign o_address = address;

   always @(posedge i_clock or posedge i_reset) begin
      if(i_reset)
        address <= 4'b0000;
      else if(i_enable_in)
        address <= i_address;
   end
   
endmodule // memory_address_register
