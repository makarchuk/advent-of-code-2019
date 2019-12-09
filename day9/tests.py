import unittest
import main

class TestCase(unittest.TestCase):
    def test_quine(self):
        program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        computer = main.IntcodeV3(program[:])
        computer.run([])
        self.assertEqual(program, computer.get_output())

    def test_big_number(self):
        program = [1102,34915192,34915192,7,4,7,99,0]
        computer = main.IntcodeV3(program[:])
        computer.run([])
        self.assertEqual(len(str(computer.get_output()[-1])), 16)

    def test_big_number_in_the_middle(self):
        program = [104,1125899906842624,99]
        computer = main.IntcodeV3(program[:])
        computer.run([])
        self.assertEqual(computer.get_output()[-1], 1125899906842624)
