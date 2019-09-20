"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #Add list properties to the CPU class to hold 256 bytes of memory 
        self.ram = [0] * 256
        #and 8 general-purpose registers.
        self.reg = [0] * 8
        #stores program counter
        self.PC = self.reg[0]
        #stores a flag
        self.FL = self.reg[4]
        #stores stack pointer
        self.SP = self.reg[7]
        #run stack from 244-255
        self.SP = 244
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b01000110: self.pop,
            0b01000101: self.push,
            0b01010000: self.call,
            0b00010001: self.ret
        }
    
    def ram_read(self, address):
        #ram_read() should accept the address to read and return the value stored there.
        return self.ram[address]
    
    def ram_write(self, value, address):
        #raw_write() should accept a value to write, and the address to write it to.
        self.ram[address] = value
    
    def hlt(self, operand_a, operand_b):
        return (0, False)

    def ldi(self, operand_a, operand_b):
        #sets register to value
        self.reg[operand_a] = operand_b
        return (3, True)

    def prn(self, operand_a, operand_b):
        #print the value at a register
        print(self.reg[operand_a])
        return (2, True)

    def mul(self, operand_a, operand_b):
        #multiply two values and store in first register
        self.alu("MUL", operand_a, operand_b)
        return (3, True)
    
    def pop(self, operand_a, operand_b):
        #get value from memory at stack pointer
        value = self.ram_read(self.SP)
        #write value to indicated spot in register
        self.reg[operand_a] = value
        #increment SP to next spot in stack memory
        self.SP += 1
        return (2, True)
    
    def push(self, operand_a, operand_b):
        #decrement SP to next spot in stack memory
        self.SP -= 1
        #get value from indicated spot in register
        value = self.reg[operand_a]
        #write value to RAM at SP
        self.ram_write(value, self.SP)
        return(2, True)

    def load(self, program):
        """Load a program into memory."""
        try:
            address = 0
            with open(program) as f:
                for line in f:
                    comment_split = line.split("#")
                    number = comment_split[0].strip()
                    if number == "":
                        continue
                    value = int(number, 2)
                    self.ram_write(value, address)
                    address += 1
        except FileNotFoundError:
            print(f"{program} not found")
            sys.exit(2)
        if len(sys.argv) != 2:
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a]) * (self.reg[reg_b])
            return 2
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            #if-else cascade for actions
            IR = self.ram[self.PC]
            #setting operand a and b
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)            
            try:
                #halt the program if instruction register matches halt value
                operation_output = self.commands[IR](operand_a, operand_b)
                #set value of instruction register to integer
                running = operation_output[1]
                self.PC += operation_output[0]
            except:
                #handle error
                print("Unknown command")
                sys.exit(1)

