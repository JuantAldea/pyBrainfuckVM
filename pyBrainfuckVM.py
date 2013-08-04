# pyBrainfuckVM is a virtual machine for the brainfuck language
# Copyright (C) 2013, Juan Antonio Aldea Armenteros
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re
import sys

class BrainfuckVM:

    class BrainfuckVMException(Exception):

        def __init__(self):
            pass

        def __str__(self):
            return repr(self.value)

    class MemoryPointerUnderflow(BrainfuckVMException):

        def __init__(self):
            self.value = "MemoryPointerUnderflow"

    class MemoryPointerOverflow(BrainfuckVMException):

        def __init__(self):
            self.value = "MemoryPointerOverflow"

    class ProgramPointerUnderflow(BrainfuckVMException):

        def __init__(self):
            self.value = "ProgramPointerUnderflow"

    class ProgramPointerOverflow(BrainfuckVMException):

        def __init__(self):
            self.value = "ProgramPointerOverflow"

    class InvalidOperation(BrainfuckVMException):

        def __init__(self):
            self.value = "InvalidOperation"

    def __init__(self, heap_size):
        self.heap_size = 30000 if heap_size < 30000 else heap_size
        self.memory = [0 for i in range(self.heap_size)]
        self.data_pointer = 0
        self.program_counter = 0

    def check_memory_overflow(self):
        if (self.data_pointer >= self.heap_size):
            raise self.MemoryPointerOverflow()

    def check_memory_underflow(self):
        if (self.data_pointer < 0):
            raise self.MemoryPointerUnderflow()

    def op_major(self):
        self.data_pointer += 1
        self.check_memory_overflow()

    def op_minor(self):
        self.data_pointer -= 1
        self.check_memory_underflow()

    def op_plus(self):
        self.memory[self.data_pointer] = min(255, self.memory[self.data_pointer] + 1)

    def op_minus(self):
        self.memory[self.data_pointer] = max(0, self.memory[self.data_pointer] - 1)

    def op_point(self):
        sys.stdout.write(chr(self.memory[self.data_pointer]))

    def op_comma(self):
        self.memory[self.data_pointer] = max(min(255, input(), 0))

    def op_open_bracket(self):
        if (self.memory[self.data_pointer] == 0):
            unbalance = 1
            i = self.program_counter

            while (i < self.heap_size and unbalance > 0):
                i += 1
                if self.memory[i] == ord(']'):
                    unbalance -= 1
                elif self.memory[i] == ord('['):
                    unbalance += 1

            if i >= self.heap_size:
                raise self.ProgramPointerOverflow()
            elif unbalance == 0:
                if (i + 1 >= self.heap_size):
                    raise self.ProgramPointerOverflow()
                else:
                    self.program_counter = i

    def op_close_bracket(self):
        if (self.memory[self.data_pointer] != 0):
            unbalance = -1
            i = self.program_counter

            while (i >= 0 and unbalance < 0):
                i -= 1
                if self.memory[i] == ord(']'):
                    unbalance -= 1
                elif self.memory[i] == ord('['):
                    unbalance += 1

            if i < 0:
                raise self.ProgramPointerUnderflow()
            elif unbalance == 0:
                if (i + 1 >= self.heap_size):
                    raise self.ProgramPointerOverflow()
                else:
                    self.program_counter = i

    def load_program(self, program, load_address):
        operation_re = re.compile("[\<\>\+\-\,\.\[\]]")
        for i in range(len(program)):
            if load_address < 0:
                raise self.MemoryPointerUnderflow()
            elif load_address >= self.heap_size:
                raise self.MemoryPointerOverflow()
            if operation_re.match(program[i]):
                self.memory[load_address] = ord(program[i])
                load_address += 1
            else:
                print "PARSER ERROR: ", program[i]
        # eof mark
        self.memory[load_address] = -1

    def run_step(self):
        if self.program_counter >= self.heap_size:
            raise self.ProgramPointerOverflow()
        instruction = self.memory[self.program_counter]
        if instruction == ord(">"):
            self.op_major()
        elif instruction == ord("<"):
            self.op_minor()
        elif instruction == ord("+"):
            self.op_plus()
        elif instruction == ord("-"):
            self.op_minus()
        elif instruction == ord('.'):
            self.op_point()
        elif instruction == ord(','):
            self.op_comma()
        elif instruction == ord('['):
            self.op_open_bracket()
        elif instruction == ord(']'):
            self.op_close_bracket()
        elif instruction == -1:
            self.running = False
        else:
            raise self.InvalidOperation()
        self.program_counter += 1

    def run_program(self, program_address):
        self.running = True
        self.program_counter = program_address
        while self.running:
            self.run_step()

    def dump(self):
        sys.stdout.write("PC: " + str(self.program_counter) + "\n")
        sys.stdout.write("Program address: " + str(self.program_counter) + "\n")
        sys.stdout.write("Data address: " + str(self.data_pointer) + "\n")
        for i in range(self.heap_size):
            sys.stdout.write(str(self.memory[i]))

    def peek(self, index):
        if index >= self.heap_size:
            raise self.MemoryPointerOverflow
        elif index < 0:
            raise self.MemoryPointerUnderflow
        return self.memory[index]

    def poke(self, index, byte):
        if index >= self.heap_size:
            raise self.MemoryPointerOverflow
        elif index < 0:
            raise self.MemoryPointerUnderflow
        self.memory[index] = byte

def main():
    machine = BrainfuckVM(150)
    machine.load_program("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.", 6)
    machine.run_program(6)

if __name__ == "__main__":
    main()    
