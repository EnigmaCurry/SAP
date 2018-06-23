/**
 * 16 Byte RAM
 */
module ram_16x8
  (
   input       i_program_mode, // 0==run program, 1==manual input data
   input [7:0] i_data_program, // dedicated programming switches for manual input
   input [3:0] i_address,      // address to read/write from/to
   input       i_write_enable, // Enable writing (supercedes i_read_enable)
   input       i_read_enable,  // Enable reading (if neither read nor write, disconnect io_data)
   inout [7:0] io_data         // The main wbus connection for input and output
   );

   reg [7:0]    ram [0:15];
   reg [7:0]   out;
   assign io_data = (i_read_enable) ? out : 8'bzzzzzzzz;

   integer     index;
   initial begin
      for(index = 0; index < 16; index=index+1) begin
         ram[index]  = 8'b00000000;
      end
   end

   always @* begin
      if(i_write_enable && i_program_mode) begin
         // Write to i_address in RAM from the data found on the i_data_program bus
         ram[i_address] <= i_data_program;
      end
      else if(i_write_enable) begin
         // Write to i_address in RAM from the data found on the io_data bus
         ram[i_address] <= io_data;
      end
      out <= ram[i_address];        
   end
   
   
endmodule // ram_16x8
