import itertools
from collections import defaultdict

class Intcode():
    def __init__(self, memory):
        self.memory = memory
        self.cursor = 0
        self._input = []
        self._output = []
        self.instructions = {
            1: self.sum_instruction,
            2: self.multiplication_instruction,
            3: self.input_instruction,
            4: self.output_instruction,
            99: self.exit_instruction
        }
        super().__init__()

    def run(self, input=None):
        if input is not None:
            self._input = input
        res = self.tick()
        while not res:
            res = self.tick()
        return res

    def output(self, val):
        self._output.append(val)

    def get_output(self):
        return self._output

    def pop_input(self):
        return self._input.pop()

    def set_memory(self, pos, val):
        self.memory[pos] = val

    def get(self, position):
        return self.memory[position]

    def pop(self):
        val = self.memory[self.cursor]
        self.cursor += 1
        return val

    def pop_instruction(self):
        instruction = self.pop()
        encoded_modes, op = divmod(instruction, 100)
        modes = {i: int(x) for i, x in enumerate(reversed(str(encoded_modes)))}
        return op, modes

    def tick(self):
        instruction, modes = self.pop_instruction()
        handler = self.instructions.get(instruction)
        if handler is not None:
            return handler(modes)
        else:
            raise Exception("Unknown instruction: {}".format(instruction))

    def sum_instruction(self, modes):
        left = self.get_arg(self.pop(), modes.pop(0, 0))
        right = self.get_arg(self.pop(), modes.pop(1, 0))
        output_position = self.output_position(self.pop(), modes.pop(2, 0))
        self.set_memory(output_position, left + right)
        return False

    def multiplication_instruction(self, modes):
        left = self.get_arg(self.pop(), modes.pop(0, 0))
        right = self.get_arg(self.pop(), modes.pop(1, 0))
        output_position = self.output_position(self.pop(), modes.pop(2, 0))
        self.set_memory(output_position, left * right)
        return False

    def input_instruction(self, modes):
        output_position = self.output_position(self.pop(), modes.pop(0, 0))
        val = self.pop_input()
        self.set_memory(output_position, val)
        return False

    def output_position(self, arg, mode):
        if mode == 0:
            return arg
        raise AssertionError("Immediate mode for output?")

    def output_instruction(self, modes):
        val = self.get_arg(self.pop(), modes.pop(0, 0))
        self.output(val)
        return False

    def exit_instruction(self, modes):
        return True

    def get_arg(self, arg, mode):
        if mode == 0:
            return self.get(arg)
        if mode == 1:
            return arg
        else:
            raise Exception("Expected a mode to be 0 or 1. Found={}".format(mode))

class Jumper(Intcode):
    def __init__(self, memory):
        super().__init__(memory)
        self.instructions.update(
            {
                5: self.jump_if_true_instruction,
                6: self.jump_if_false_instruction,
                7: self.less_then_instruction,
                8: self.equals_instruction,
            }
        )

    def set_cursor(self, pointer):
        self.cursor = pointer

    def jump_if_true_instruction(self, modes):
        condition = self.get_arg(self.pop(), modes.pop(0, 0))
        pointer = self.get_arg(self.pop(), modes.pop(1, 0))
        if condition != 0:
            self.set_cursor(pointer)

    def jump_if_false_instruction(self, modes):
        condition = self.get_arg(self.pop(), modes.pop(0, 0))
        pointer = self.get_arg(self.pop(), modes.pop(1, 0))
        if condition == 0:
            self.set_cursor(pointer)

    def less_then_instruction(self, modes):
        left = self.get_arg(self.pop(), modes.pop(0, 0))
        right = self.get_arg(self.pop(), modes.pop(1, 0))
        output_position = self.output_position(self.pop(), modes.pop(2, 0))
        self.set_memory(output_position, int(left < right))
        return False

    def equals_instruction(self, modes):
        left = self.get_arg(self.pop(), modes.pop(0, 0))
        right = self.get_arg(self.pop(), modes.pop(1, 0))
        output_position = self.output_position(self.pop(), modes.pop(2, 0))
        self.set_memory(output_position, int(left == right))
        return False

class IntcodeV3(Jumper):
    def __init__(self, memory):
        super().__init__(memory)
        self.memory = defaultdict(
            lambda : 0,
            {i: v for i, v in enumerate(self.memory)}
        )
        self.relative_base = 0
        self.instructions.update({
            9: self.adjust_base_instruction
        })

    def adjust_base_instruction(self, modes):
        self.relative_base += self.get_arg(self.pop(), modes.pop(0, 0))
        return False

    def get_arg(self, arg, mode):
        if mode == 2:
            return self.get(self.relative_base + arg)
        return super().get_arg(arg, mode)

    def output_position(self, arg, mode):
        if mode == 2:
            return self.relative_base + arg
        return super().output_position(arg, mode)

def part1(program):
    computer = IntcodeV3(program)
    computer.run([1])
    return computer.get_output()


def part2(program):
    computer = IntcodeV3(program)
    computer.run([2])
    return computer.get_output()

if __name__ == "__main__":
    with open('input') as f:
        memory = [int(x) for x in f.read().strip().split(',')]
        print(part1(memory[:]))
        print(part2(memory[:]))