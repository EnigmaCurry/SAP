/**
 * 4 bit memory address register - MAR
 */
module memory_address_register
  (
   input        i_debug,
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

   always @(i_address or posedge i_enable_in) begin
      if(i_enable_in) begin
         address <= i_address;
         if(i_debug) $display("DEBUG: MAR load address: %b", i_address);
      end
   end
   always @(posedge i_reset) begin
      address <= 4'b0000;
      if(i_debug) $display("DEBUG: MAR reset: %b", 4'b0000);
   end
   
endmodule // memory_address_register
