import itertools

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
        output_position = self.pop()
        assert modes.pop(2, 0) == 0, "Immediate mode for output?"
        self.set_memory(output_position, left + right)
        return False

    def multiplication_instruction(self, modes):
        left = self.get_arg(self.pop(), modes.pop(0, 0))
        right = self.get_arg(self.pop(), modes.pop(1, 0))
        output_position = self.pop()
        assert modes.pop(2, 0) == 0, "Immediate mode for output?"
        self.set_memory(output_position, left * right)
        return False

    def input_instruction(self, modes):
        output_position = self.pop()
        assert modes.pop(0, 0) == 0, "Immediate mode for output?"
        val = self.pop_input()
        self.set_memory(output_position, val)
        return False

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
        output_position = self.pop()
        assert modes.pop(2, 0) == 0, "Immediate mode for output?"
        self.set_memory(output_position, int(left < right))
        return False

    def equals_instruction(self, modes):
        left = self.get_arg(self.pop(), modes.pop(0, 0))
        right = self.get_arg(self.pop(), modes.pop(1, 0))
        output_position = self.pop()
        assert modes.pop(2, 0) == 0, "Immediate mode for output?"
        self.set_memory(output_position, int(left == right))
        return False

class ChainedJumper(Jumper):
    def input_instruction(self, modes):
        if len(self._input) > 0:
            return super().input_instruction(modes)
        else:
            self.cursor -= 1
            # Something truthy to halt `run` function, but not true,
            # so we can tell the difference between input block and stop
            return object()

    def run(self, input=None):
        if input is not None:
            if self._input is not None:
                self._input = []
            input.extend(self._input)
            self._input = input
        res = self.tick()
        while not res:
            res = self.tick()
        return res


class AmplifierSequence():
    def __init__(self, program):
        super().__init__()
        self.program = program

    def range(self):
        return range(0, 5)

    def best_sequence(self):
        def sequences():
            for sequence in itertools.permutations(list(self.range()), 5):
                output = self.output(sequence)
                yield output, sequence
        results = list(sequences())
        best_sequence = max(results, key=lambda x: x[0])
        return best_sequence

    def output(self, sequence):
        signal = 0
        for phase in sequence:
            computer = Jumper(self.program[:])
            #Input reading implemented as `.pop()`, so reversing an order
            computer.run([signal, phase])
            signal = computer.get_output()[-1]
        return signal

class ChainedAmplifierSequence(AmplifierSequence):
    def __init__(self, program):
        super().__init__(program)

    def range(self):
        return range(5, 10)

    def output(self, sequence):
        interpreters = [ChainedJumper(self.program[:]) for _ in range(5)]
        output = [0]
        for iteration in itertools.count():
            for i, interpreter, setting in zip(range(5), interpreters, sequence):
                if interpreter is None:
                    if i == 0:
                        return output[0]
                    raise Exception("Interpreter is called after halting #{}".format(i))
                if iteration == 0:
                    #Reverse, because stack
                    result = interpreter.run([*output, setting])
                else:
                    result = interpreter.run(output)
                output = interpreter.get_output()[::-1]
                interpreter._output = []
                if result is True:
                    if i == 4:
                        return output[0]
                    else:
                        interpreters[i] = None

if __name__ == "__main__":
    with open('input') as f:
        memory = [int(x) for x in f.read().strip().split(',')]
        seq = AmplifierSequence(memory)
        print(seq.best_sequence())
        seq = ChainedAmplifierSequence(memory)
        print(seq.best_sequence())
