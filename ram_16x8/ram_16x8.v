/**
 * 16 Byte RAM
 */
module ram_16x8
  (
   input       i_debug,
   input       i_program_mode, // 0==run program, 1==manual input data
   input [7:0] i_program_data, // dedicated programming switches for manual input
   input [3:0] i_address, // address to read/write from/to
   input       i_write_enable, // Enable writing (supercedes i_read_enable)
   input       i_read_enable, // Enable reading (if neither read nor write, disconnect io_data)
   inout [7:0] io_data         // The main wbus connection for input and output
   );

   reg [7:0]    ram [0:15];
   assign io_data = (i_read_enable) ? ram[i_address] : 8'bzzzzzzzz;

   // For simplicity, we can initialize all of the RAM in hardware,
   // it's only 16B. However, this does not scale well.
   integer     index;
   initial begin
      for(index = 0; index < 16; index=index+1) begin
         ram[index]  = 8'b00000000;
      end
   end

   always @(posedge i_write_enable) begin
      if(i_program_mode) begin
         // Write to i_address in RAM from the data found on the i_program_data bus
         if(i_debug) $display("DEBUG: Program RAM address: %b data: %b",i_address, i_program_data);
         ram[i_address] <= i_program_data;
      end else begin
         // Write to i_address in RAM from the data found on the io_data bus
         if(i_debug) $display("DEBUG: RAM write address: %b data: %b",i_address, io_data);
         ram[i_address] <= io_data;         
      end
   end

   always @(posedge i_read_enable) begin
      if(i_debug) $display("DEBUG: RAM read address: %b data to bus: %b",i_address, ram[i_address]);
   end
      
endmodule // ram_16x8
