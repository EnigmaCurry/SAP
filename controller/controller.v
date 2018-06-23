/**
 * Control-Sequencer for SPA-1+
 */
module controller
  (
   input        i_clock,
   input        i_reset,
   // Input opcode from Instruction Register
   input [3:0]  i_opcode,
   // Input from flags register
   input        i_flag_carry,
   input        i_flag_zero, 
   // Control signals:
   // upper control byte:
   output       o_halt,
   output       o_memory_address_in,
   output       o_ram_in,
   output       o_ram_out,
   output       o_instruction_in,
   output       o_instruction_out,
   output       o_register_a_in,
   output       o_register_a_out,
   // lower control byte:
   output       o_alu_out,
   output       o_alu_subtract,
   output       o_register_b_in,
   output       o_register_output_in,
   output       o_program_counter_increment,
   output       o_program_counter_out,
   output       o_program_counter_jump,
   output       o_register_flags_in,
   // debug output step:
   output [2:0] o_step
   );

   // Instruction opcodes:
   integer     NOP = 0;
   integer     LDA = 1;
   integer     ADD = 2;
   integer     SUB = 3;
   integer     STA = 4;
   integer     LDI = 5;
   integer     JMP = 6;
   integer     JC = 7;
   integer     JZ = 8;
   integer     OUT = 14;
   integer     HLT = 15;
   
   // Keep track of the current step (t-state)
   // Step 0,1 are used for Fetch Instruction
   // Step 2,3,4 are used for Execute Instruction
   reg [2:0]   step = 0;
   // o_step is a debug output, it shows the step number for the next cycle
   assign o_step = step;
   
   // 16 control bits:
   reg [15:0]   control_bits = 16'b0000_0000_0000_0000;   
   assign o_halt = control_bits[15];
   assign o_memory_address_in = control_bits[14];
   assign o_ram_in = control_bits[13];
   assign o_ram_out = control_bits[12];
   assign o_instruction_in = control_bits[11];
   assign o_instruction_out = control_bits[10];
   assign o_register_a_in = control_bits[9];
   assign o_register_a_out = control_bits[8];
   assign o_alu_out = control_bits[7];
   assign o_alu_subtract = control_bits[6];
   assign o_register_b_in = control_bits[5];
   assign o_register_output_in = control_bits[4];
   assign o_program_counter_increment = control_bits[3];
   assign o_program_counter_out = control_bits[2];
   assign o_program_counter_jump = control_bits[1];
   assign o_register_flags_in = control_bits[0];
   
   always @(posedge i_clock or posedge i_reset) begin
      if(i_reset) begin
         step <= 0;
      end
      else if(!o_halt) begin
         // Fetch Cycle
         // Common to all instructions:
         if (step == 0)
           begin
              // Fetch cycle step 0
              // Program Counter Out
              // Memory Register In
              control_bits <= 16'b0100_0000_0000_0100;
              step <= step + 1;
           end
         else if (step == 1)
           begin
              // Fetch cycle step 1
              // Instruction In
              // Ram Out
              // Program Counter Increment
              control_bits <= 16'b0001_0100_0000_1000;
              step <= step + 1;
           end
         // Instruction Cycle
         // Instruction has been loaded from RAM, now to execute it:
         // Fetch took cylces 0,1 so we are now at step 2:
         else
           begin
              case(i_opcode)
                NOP:
                  begin
                     control_bits <= 16'b0000_0000_0000_0000;
                     step <= 0; //done
                  end
                LDA:
                  begin
                     case (step)
                       2:
                         begin
                            // LDA step 2
                            // Instruction Out
                            // Memory Register In
                            control_bits <= 16'b0100_1000_0000_0000;
                            step <= step + 1;
                         end 
                      3:
                         begin
                            // LDA step 3
                            // Ram Out
                            // Register A In
                            control_bits <= 16'b0001_0010_0000_0000;
                            step <= 0; // done
                         end
                     endcase
                  end // case: LDA
                ADD:
                  begin
                     case (step)
                       2:
                         begin
                            // ADD step 2
                            // Instruction Out
                            // Memory Register In
                            control_bits <= 16'b0100_1000_0000_0000;
                            step <= step + 1;
                         end
                       3:
                         begin
                            // ADD step 3
                            // Ram Out
                            // Register B In
                            control_bits <= 16'b0001_0000_0010_0000;
                            step <= step + 1;
                         end
                       4:
                         begin
                            // ADD step 4
                            // ALU Out
                            // Register A In
                            // Flags In
                            control_bits <= 16'b0000_0010_1000_0001;
                            step <= 0; // done
                         end
                     endcase // case (step)
                  end
                SUB:
                  begin
                     case (step)
                       2:
                         begin
                            // SUB step 2
                            // Instruction Out
                            // Memory Register In
                            control_bits <= 16'b0100_1000_0000_0000;
                            step <= step + 1;
                         end
                       3:
                         begin
                            // SUB step 3
                            // Ram Out
                            // Register B In
                            control_bits <= 16'b0001_0000_0010_0000;
                            step <= step + 1;
                         end
                       4:
                         begin
                            // SUB step 4
                            // ALU Subtract
                            // ALU Out
                            // Register A In
                            // Flags In
                            control_bits <= 16'b0000_0010_1100_0001;
                            step <= 0; // done
                         end
                     endcase // case (step)
                  end
                STA:
                  begin
                     case (step)
                       2:
                         begin
                            // STA step 2
                            // Instruction Out
                            // Memory Register In
                            control_bits <= 16'b0100_1000_0000_0000;
                            step <= step + 1;
                         end
                       3:
                         begin
                            // STA step 3
                            // Register A Out
                            // Ram In
                            control_bits <= 16'b0010_0001_0000_0000;
                            step <= 0; // done
                         end
                     endcase // case (step)
                  end // case: STA
                LDI:
                  begin
                     case (step)
                       2:
                         begin
                            // LDI step 2
                            // Instruction Out
                            // Register A In
                            control_bits <= 16'b0000_1010_0000_0000;
                            step <= 0; // done
                         end
                     endcase // case (step)
                  end
                JMP:
                  begin
                     case (step)
                       2:
                         begin
                            // JMP step 2
                            // Instruction Out
                            // Jump
                            control_bits <= 16'b0000_1000_0000_0010;
                            step <= 0; // done
                         end
                     endcase // case (step)
                  end
                JC:
                  begin
                     case (step)
                       2:
                         begin
                            //JC step 2
                            if (i_flag_carry) begin
                               // On Carry:
                               // Instruction Out
                               // Jump
                               control_bits <= 16'b0000_1000_0000_0010;
                               step <= 0; // done
                            end
                            else begin
                               // Else NOP
                               control_bits <= 16'b0000_0000_0000_0000;
                               step <= 0; // done
                            end
                         end // case: 2
                     endcase
                  end
                JZ:
                  begin
                     case (step)
                       2:
                         begin
                            //JZ step 2
                            if (i_flag_zero) begin
                               // On Zero:
                               // Instruction Out
                               // Jump
                               control_bits <= 16'b0000_1000_0000_0010;
                               step <= 0; // done
                            end
                            else begin
                               // Else NOP
                               control_bits <= 16'b0000_0000_0000_0000;
                               step <= 0; // done
                            end
                         end // case: 2
                     endcase
                  end
                OUT:
                  begin
                     case (step)
                       2:
                         begin
                            // OUT step 2
                            // Register A Out
                            // Output Register In
                            control_bits <= 16'b0000_0001_0001_0000;
                            step <= 0; // done
                         end
                     endcase // case (step)                     
                  end
                HLT:
                  begin
                     case (step)
                       2:
                         begin
                            // HLT
                            // Halt Out
                            control_bits <= 16'b1000_0000_0000_0000;
                            step <= 0; // done
                         end
                     endcase // case (step)
                  end
              endcase // case (i_opcode)
           end // else: !if(step == 1)
      end // else: !if(i_reset)
   end // always @ (posedge i_clock or posedge i_reset)
endmodule // controller
