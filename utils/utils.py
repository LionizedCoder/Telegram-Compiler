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


def lines_output(output):
    return [escape_ansi(line['text']) for line in output]


def escape_ansi(text):
    """Remove ANSI escape codes"""
    text = re.sub(r'\x1b\[([\d;]*?)m', '', text)
    text = text.replace('\x1b[K', '')
    return text