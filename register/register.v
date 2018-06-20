/**
 * 8 bit register
 * Used in Accumulator and B register
 */
module register
  (
   input        i_clock,
   input        i_load_data,
   input        i_send_data,
   input        i_reset,
   input [7:0]  i_bus,
   output [7:0] o_bus,
   output [7:0] o_unbuffered
   );

   reg [7:0]   data;
   
   assign o_bus = i_send_data ? data : 8'bzzzzzzzz;
   assign o_unbuffered = data;   

   always @(posedge i_clock or posedge i_reset) begin
      if(i_reset) begin
         data <= 8'bzzzzzzzz;
      end 
      else if(i_load_data) begin
         data <= i_bus;
      end
   end
   
   
endmodule // register

