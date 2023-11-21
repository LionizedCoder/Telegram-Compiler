from dataclasses import dataclass
from enum import Flag, auto
import re


class OutputKind(Flag):
    ASM = auto()
    OUTPUT = auto()
    ALL = ASM | OUTPUT

@dataclass
class CompileResult:
    ok: bool
    header: str
    asm: list[str]
    output: list[str]
    
    def to_messages(self, kind: OutputKind):
        w = MessageWriter()
        w.add_line(self.header)

        if kind & OutputKind.ASM:
            if not self.asm:
                w.add_line('*Assembly*: void')
            else:
                w.add_line('*Assembly:*')
                w.set_code_mode()
                for line in self.asm:
                    w.add_line(line)
                w.set_plain_mode()

        if kind & OutputKind.OUTPUT:
            if not self.output:
                w.add_line('*Output*: void')
            else:
                w.add_line('*Output*:')
                w.set_code_mode()
                for line in self.output:
                    w.add_line(line)
                w.set_plain_mode()
        return w.messages

class MessageWriter:
    def __init__(self, max_size: int = 4096) -> None:
        self.max_size = max_size
        self.messages = [""]
        self.code_mode = False

    def add_line(self, line: str) -> None:
        line = line + "\n"
        while len(line) > self.max_size:
            self._add_block(line[:self.max_size])
            line = line[self.max_size:]
        self._add_block(line)

    def set_code_mode(self) -> None:
        self.messages[-1] += "```\n"
        self.code_mode = True

    def set_plain_mode(self) -> None:
        self.messages[-1] += "```\n"
        self.code_mode = False

    def _add_block(self, line: str) -> None:
        if len(self.messages[-1]) + len(line) > self.max_size:
            if self.code_mode:
                self.messages[-1] += "```\n"
            self.messages.append("")
            if self.code_mode:
                self.messages[-1] += "```\n"
        self.messages[-1] += line



def lines_output(output):
    return [escape_ansi(line['text']) for line in output]


def escape_ansi(text):
    """Remove ANSI escape codes"""
    text = re.sub(r'\x1b\[([\d;]*?)m', '', text)
    text = text.replace('\x1b[K', '')
    return text