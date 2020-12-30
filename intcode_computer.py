import operator
from collections import defaultdict, deque
from typing import Callable, Dict, Iterator, List, Optional, Tuple
from enum import Enum


class OpCode(Enum):
    END = 99
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    MOVE_RELATIVE_BASE = 9


def get_param_mode(param_modes: int, param_num: int) -> int:
    return (param_modes // (10 ** param_num)) % 10


class Program(Iterator[int]):
    def __init__(self, program: List[int], input_data: Optional[List[int]] = None) -> None:
        self.program = program
        self.extra_memory: Dict[int, int] = defaultdict(int)
        self.pointer = 0
        self.relative_base = 0
        self.input = deque(input_data if input_data is not None else [])
        self.ended = False

    def __next__(self) -> int:
        result = self.next_output_or_end()
        if result is None:
            raise StopIteration()
        return result

    def __getitem__(self, idx: int) -> int:
        if idx < len(self.program):
            return self.program[idx]
        else:
            return self.extra_memory[idx]

    def __setitem__(self, idx: int, val: int) -> None:
        if idx < len(self.program):
            self.program[idx] = val
        else:
            self.extra_memory[idx] = val

    def peek(self) -> int:
        return self[self.pointer]

    def next_mem(self) -> int:
        item = self[self.pointer]
        self.pointer += 1
        return item

    def read(self, num: int) -> List[int]:
        result = []
        for _ in range(num):
            result.append(self.next_mem())
        return result

    def jump(self, pointer: int) -> None:
        self.pointer = pointer

    def move_relative_base(self, offset: int) -> None:
        self.relative_base += offset

    def get_input_arg_value(self, param_num: int, param_modes: int, idx: int) -> int:
        param_mode = get_param_mode(param_modes, param_num)
        if param_mode == 1:
            return idx
        elif param_mode == 2:
            return self[self.relative_base + idx]
        else:
            return self[idx]

    def get_output_arg_position(self, param_num: int, param_modes: int, idx: int) -> int:
        param_mode = get_param_mode(param_modes, param_num)
        if param_mode == 2:
            return self.relative_base + idx
        else:
            return idx

    def get_args(self, param_modes: int, input_args: int = 0, output_args: int = 0) -> Tuple[int, ...]:
        raw_args = self.read(input_args + output_args)
        result_input_args = [self.get_input_arg_value(i, param_modes, raw_arg) for i, raw_arg in enumerate(raw_args[:input_args])]
        result_output_args = [self.get_output_arg_position(i + input_args, param_modes, raw_arg) for i, raw_arg in enumerate(raw_args[input_args:])]
        return tuple(result_input_args + result_output_args)

    def get_input_arg(self, param_modes: int) -> int:
        return self.get_args(param_modes, 1, 0)[0]

    def get_output_arg(self, param_modes: int) -> int:
        return self.get_args(param_modes, 0, 1)[0]

    def next_command(self) -> Tuple[bool, Optional[int]]:
        if self.ended:
            raise Exception("Tried to run after program ended")
        input_data = None
        item = self.next_mem()

        param_mode, op_val = divmod(item, 100)
        op = OpCode(op_val)
        if op == OpCode.END:
            self.ended = True
            return (True, None)
        elif op == OpCode.INPUT:
            if len(self.input) == 0:
                raise Exception("Program asked for input but none was available")
            input_data = self.input.popleft()
        output = op_dispatch[op](self, param_mode, input_data)
        return (False, output)

    def next_output_or_end(self) -> Optional[int]:
        while True:
            reached_end, output = self.next_command()
            if reached_end:
                return None
            if output is not None:
                return output

    def run_until_input(self) -> Iterator[int]:
        while self.peek() % 100 != OpCode.INPUT.value:
            reached_end, output = self.next_command()
            if reached_end:
                return
            elif output is not None:
                yield output

    def run_to_end(self) -> None:
        while self.next_output_or_end() is not None:
            pass

    def next_output(self) -> int:
        result = self.next_output_or_end()
        if result is None:
            raise Exception("Expected output but reached end of program")
        return result

    def send_input(self, input_data: int) -> None:
        self.input.append(input_data)

    def write_string(self, input_data: str) -> None:
        for c in input_data + "\n":
            self.send_input(ord(c))

    def read_line(self) -> Optional[str]:
        line: List[str] = []
        while True:
            c_val = self.next_output_or_end()
            if c_val is None:
                return None
            c = chr(c_val)
            if c == "\n":
                return "".join(line)
            line.append(c)

    def read_lines(self) -> Iterator[str]:
        while True:
            s = self.read_line()
            if s is None:
                break
            yield s


FuncType = Callable[..., Optional[int]]


def run_binary_operator(op: Callable[[int, int], int], program: Program, param_modes: int) -> None:
    arg1, arg2, output = program.get_args(param_modes, 2, 1)
    program[output] = op(arg1, arg2)


def run_binary_comparitor(op: Callable[[int, int], bool], program: Program, param_modes: int) -> None:
    arg1, arg2, output = program.get_args(param_modes, 2, 1)
    program[output] = 1 if op(arg1, arg2) else 0


def run_input_operator(program: Program, input_data: int, param_modes: int) -> None:
    program[program.get_output_arg(param_modes)] = input_data


def run_output_operator(program: Program, param_modes: int) -> int:
    return program.get_input_arg(param_modes)


def run_jump(eq: bool, program: Program, param_modes: int) -> None:
    arg, dest = program.get_args(param_modes, input_args=2)
    if (arg != 0) == eq:
        program.jump(dest)


def move_relative_base(program: Program, param_mode: int) -> None:
    program.move_relative_base(program.get_input_arg(param_mode))


op_dispatch: Dict[OpCode, Callable[[Program, int, int], Optional[int]]] = {
    OpCode.ADD: lambda program, param_mode, input_data: run_binary_operator(operator.add, program, param_mode),
    OpCode.MUL: lambda program, param_mode, input_data: run_binary_operator(operator.mul, program, param_mode),
    OpCode.INPUT: lambda program, param_mode, input_data: run_input_operator(program, input_data, param_mode),
    OpCode.OUTPUT: lambda program, param_mode, input_data: run_output_operator(program, param_mode),
    OpCode.JUMP_IF_TRUE: lambda program, param_mode, input_data: run_jump(True, program, param_mode),
    OpCode.JUMP_IF_FALSE: lambda program, param_mode, input_data: run_jump(False, program, param_mode),
    OpCode.LESS_THAN: lambda program, param_mode, input_data: run_binary_comparitor(operator.lt, program, param_mode),
    OpCode.EQUALS: lambda program, param_mode, input_data: run_binary_comparitor(operator.eq, program, param_mode),
    OpCode.MOVE_RELATIVE_BASE: lambda program, param_mode, input_data: move_relative_base(program, param_mode)
}


def run(program_lines: List[int], input_list: Optional[List[int]] = None) -> Optional[int]:
    result = run_to_end(program_lines, input_list)
    return result[-1] if result else None


def run_to_end(program_lines: List[int], input_list: Optional[List[int]] = None) -> List[int]:
    return list(Program(program_lines, input_list))
