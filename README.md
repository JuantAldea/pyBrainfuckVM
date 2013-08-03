PyBrainfuckVM
=============

Brainfuck virtual machine written in Python 2.7

  - In this implementation both code and memory are stored in the same tape so programs can modify themselves.
  - It throws exceptions like Memory overflow/underflow. Beware, exception raise conditions set may not be complete.
  - -1 is used as END OF PROGRAM mark. It is automatically appended at the end of the program so bear in mind that your program will be longer.

The VM comes with a Hello World! example program.
