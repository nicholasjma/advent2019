from collections import deque


class IntCode:
    """IntCode class for Advent of Code 2019"""
    def __init__(self, data, input=None, verbose=False):
        if isinstance(data, str):
            with open(data) as f:
                self.l = [int(x) for x in f.read().split(",")]
        else:
            self.l = deepcopy(data)
        self.idx = 0
        if input is None:
            self.input = deque()
        else:
            self.input = deque(input)
        self.output = deque()
        self.verbose = verbose
        self.halt = False
        self.relative = 0

    def print(self, *s):
        """Print method that checks for verbosity"""
        if self.verbose:
            print(*s)

    def process_code(self, code):
        """Given instruction, return opcode and options"""
        code, opcode = divmod(code, 100)
        options = [0] * 3
        for i in range(3):
            code, options[i] = divmod(code, 10)
        return opcode, options

    def expand(self, spec):
        """Make tape bigger if needed, spec can be a slice or int"""
        if not isinstance(spec, slice):
            self.l.extend([0] * (spec - len(self) + 1))
        else:
            # get the largest value in the slice
            m = max(
                range(
                    spec.start if spec.start is not None else 0,
                    spec.stop if spec.stop is not None else len(s),
                    spec.step if spec.step is not None else 1,
                )
            )
            self.l.extend([0] * (m - len(self) + 1))

    def __setitem__(self, spec, value):
        """Set value on tape, expanding as needed"""
        try:
            self.l[spec] = value
        except IndexError:
            self.expand(spec)
            self.l[spec] = value

    def __getitem__(self, spec):
        """Get value from tape, expanding as needed"""
        try:
            return self.l[spec]
        except IndexError:
            self.expand(spec)
            return self.l[spec]

    def __len__(self):
        """Returns length of the tape"""
        return len(self.l)

    def pop(self):
        """Get the next instruction and move the current instruction pointer"""
        try:
            instruction, options = self.process_code(self.l[self.idx])
        except IndexError:
            # we ran out of instructions
            raise StopIteration
        try:
            plen = self.LENGTH[instruction]
        except KeyError:
            # bad instruction
            print(instruction, options)
            raise KeyError(instruction)
        params = self[self.idx + 1 : self.idx + plen]
        #         print("Raw instruction ", instruction, params, options)
        self.idx += plen
        # update parameters by mode
        new_params = [
            self[x]
            if mode == 0
            else x
            if mode == 1
            else self[self.relative + x]
            if mode == 2
            else ValueError("Invalid ", x, mode)
            for x, mode in zip(params, options)
        ]
        # don't dereference write positions
        if instruction in self.POS:
            if options[plen - 2] == 0:
                new_params[plen - 2] = params[plen - 2]
            elif options[plen - 2] == 2:
                new_params[plen - 2] = self.relative + params[plen - 2]
        #         print("Processed Instruction ", params)
        return instruction, new_params, self.idx - plen, self.l[self.idx - plen]

    def runinst(self):
        """Run an instruction"""
        instruction, params, i, orig = self.pop()
        if instruction == 1:
            x, y, idx = params
            self[idx] = x + y
            self.print(f"{i}: Write sum {x} + {y} to {idx}")
        elif instruction == 2:
            x, y, idx = params
            self[idx] = x * y
            self.print(f"{i}: Write product {x} * {y} to {idx}")
        elif instruction == 3:
            if len(self.input) > 0:
                self[params[0]] = self.pop_input()
            else:
                self.print("Waiting for input")
                self.idx = i
                return -1
            self.print(f"{i}: Input {self[params[0]]} to {params[0]}")
        elif instruction == 4:
            self.push_output(params[0])
            self.print(f"{i}: Output position", params[0], "value", self.output[-1])
        elif instruction == 5:
            x, idx = params
            if x > 0:
                self.idx = idx
            self.print(f"{i}: Jump to {idx} if {x} > 0")
        elif instruction == 6:
            x, idx = params
            if x == 0:
                self.idx = idx
            self.print(f"{i}: Jump to {idx} if {x} == 0")
        elif instruction == 7:
            x, y, idx = params
            self[idx] = int(x < y)
            self.print(f"{i}: Write {x} < {y} to {idx}")
        elif instruction == 8:
            x, y, idx = params
            self[idx] = int(x == y)
            self.print(f"{i}: Write {x} == {y} to {idx}")
        elif instruction == 9:
            self.relative += params[0]
        elif instruction == 99:
            self.print(f"{i}: Terminating")
            self.halt = True
        else:
            raise ValueError("Invalid instruction:", instruction, params)
        if self[i] != orig:
            # if we modified the opcide, don't advance current pointer
            self.idx -= self.LENGTH[instruction]
        return instruction

    def run_all(self):
        """Run instructions until termination or input required"""
        while True:
            inst = self.runinst()
            if inst == 99:
                return self.output
            elif inst == -1:
                return -1

    def pop_input(self):
        """Pop an input"""
        return self.input.popleft()

    def push_input(self, value):
        """Push a new input"""
        self.input.append(value)

    def pop_output(self):
        """Pop an output"""
        return self.output.popleft()

    def push_output(self, value):
        """Push a new output"""
        self.output.append(value)

    POS = {1, 2, 3, 7, 8}
    LENGTH = {1: 4, 2: 4, 99: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}
