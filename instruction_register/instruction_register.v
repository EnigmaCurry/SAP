/**
 * Instruction register
 * Two 4 bit registers: hiNib Opcode and loNib Address
 */
module instruction_register
  (
   input        i_clock,
   // Flag to load the current instruction from the bus
   input        i_load_instruction,
   // Flag to send the current Instruction Address to the bus
   input        i_send_address,
   input        i_reset,
   input [7:0]  i_bus,
   // The registered opcode, 4 high bits to go to the Instruction Decoder:
   output [3:0] o_opcode,
   // The registered address, 4 low bits to go to the bus. Tri-state
   // output, only sending data when i_send_address=1:
   output [3:0] o_address
   );

   reg [3:0]    hiNib = 4'b0000;
   reg [3:0]    loNib = 4'b0000;

   assign o_opcode = hiNib;
   assign o_address = i_send_address ? loNib : 4'bzzzz;

   always @(posedge i_clock or posedge i_reset) begin
      if(i_reset) begin
         hiNib <= 4'b0000;
         loNib <= 4'b0000;
      end 
      else if(i_load_instruction) begin
         hiNib <= i_bus[7:4];
         loNib <= i_bus[3:0];
      end
   end
   
   
endmodule // instruction_register

