/**
 * 8 bit register
 * Used in Accumulator and B register
 */
module register
  (
   input        i_debug,
   input        i_reset, 
   input        i_load_data,
   input        i_send_data,
   input [7:0]  i_bus,
   output [7:0] o_bus,
   output [7:0] o_unbuffered
   );

   reg [7:0]   data;
   
   assign o_bus = i_send_data ? data : 8'bzzzzzzzz;
   assign o_unbuffered = data;   

   always @(i_bus or posedge i_load_data) begin
      if(i_load_data) begin
         data <= i_bus;
         if(i_debug) $display("DEBUG: Register loaded: %b", i_bus);
      end
   end

   always @(posedge i_reset) begin
      data <= 8'bzzzzzzzz;
   end
   
   
endmodule // register

