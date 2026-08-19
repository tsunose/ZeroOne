"""
ZeroOne Compiler

tokens.py

Version 2.0.0
"""

from enum import Enum, auto


class TokenType(Enum):

    # ==========================
    # Basic
    # ==========================

    KEYWORD = auto()

    IDENTIFIER = auto()

    NUMBER = auto()

    STRING = auto()

    SYMBOL = auto()

    NEWLINE = auto()

    EOF = auto()


class Token:

    def __init__(
        self,
        token_type,
        value,
        line,
        column
    ):

        self.type = token_type

        self.value = value

        self.line = line

        self.column = column

    def __repr__(self):

        return (
            f"{self.type.name}"
            f"({self.value}) "
            f"[{self.line}:{self.column}]"
        )


# =====================================
# Keywords
# =====================================

CANONICAL_KEYWORDS = {
    # Variable
    "SET",

    # Output
    "OUT",

    # Condition
    "WHEN",
    "ELSE",
    "END",

    # Loop
    "LOOP",
    "BREAK",
    "CONTINUE",

    # Function
    "FUNC",
    "RETURN",

    # Program
    "EXIT",
    "IMPORT",
    "ASSET",

    # Boolean
    "TRUE",
    "FALSE",

    # Logic
    "AND",
    "OR",
    "NOT",
}

KEYWORD_ALIASES = {
    # Output/Display
    "PRINT": "OUT",
    "SHOW": "OUT",
    "VIEW": "OUT",
    "DISPLAY": "OUT",
    "ECHO": "OUT",
    "WRITE": "OUT",
    "PUT": "OUT",
    "DRAW": "OUT",
    "RENDER": "OUT",
    "POP": "OUT",
    "ALERT": "OUT",
    "NOTICE": "OUT",
    "MSG": "OUT",
    "LOG": "OUT",
    "DEBUG": "OUT",
    "TRACE": "OUT",
    "DUMP": "OUT",
    "EXPORT": "OUT",
    "SEND": "OUT",

    # Input
    "IN": "OUT",
    "INPUT": "OUT",
    "READ": "OUT",
    "GET": "OUT",
    "FETCH": "OUT",
    "SCAN": "OUT",
    "ASK": "OUT",
    "QUERY": "OUT",
    "RECEIVE": "OUT",
    "LOAD": "OUT",
    "OPEN": "OUT",
    "SELECT": "OUT",
    "CHOOSE": "OUT",
    "PICK": "OUT",
    "FIND": "OUT",
    "SEARCH": "OUT",
    "LOOK": "OUT",
    "CHECK": "OUT",
    "CAPTURE": "OUT",

    # Variables
    "LET": "SET",
    "VAR": "SET",
    "CONST": "SET",
    "DEFINE": "SET",
    "CREATE": "SET",
    "NEW": "SET",
    "COPY": "SET",
    "MOVE": "SET",
    "SWAP": "SET",
    "CLEAR": "SET",
    "RESET": "SET",
    "DELETE": "SET",
    "REMOVE": "SET",
    "SAVE": "SET",
    "STORE": "SET",
    "KEEP": "SET",
    "HOLD": "SET",
    "FREE": "SET",
    "LOCK": "SET",

    # Flow control
    "IF": "WHEN",
    "THEN": "WHEN",
    "CASE": "WHEN",
    "EQ": "WHEN",
    "NE": "WHEN",
    "GT": "WHEN",
    "LT": "WHEN",
    "GE": "WHEN",
    "LE": "WHEN",
    "AND": "AND",
    "OR": "OR",
    "NOT": "NOT",

    # Math / generic command aliases
    "ADD": "OUT",
    "SUB": "OUT",
    "MUL": "OUT",
    "DIV": "OUT",
    "MOD": "OUT",
    "INC": "OUT",
    "DEC": "OUT",
    "POWER": "OUT",
    "ROOT": "OUT",
    "ABS": "OUT",
    "ROUND": "OUT",
    "FLOOR": "OUT",
    "CEIL": "OUT",
    "MAX": "OUT",
    "MIN": "OUT",
    "AVG": "OUT",
    "SUM": "OUT",
    "COUNT": "OUT",
    "RANDOM": "OUT",
    "CLAMP": "OUT",

    # System / data aliases
    "ARRAY": "OUT",
    "LIST": "OUT",
    "TEXT": "OUT",
    "FILE": "OUT",
    "NET": "OUT",
    "SYSTEMOS": "OUT",
    "SECURE": "OUT",
    "DATA": "OUT",
    "TABLE": "OUT",
    "ROW": "OUT",
    "COLUMN": "OUT",
    "CELL": "OUT",

    # Loop
    "FOR": "LOOP",
    "WHILE": "LOOP",
    "UNTIL": "LOOP",
    "REPEAT": "LOOP",
    "FOREACH": "LOOP",
    "BREAK": "BREAK",
    "CONTINUE": "CONTINUE",
    "STOP": "EXIT",
    "PAUSE": "EXIT",
    "WAIT": "EXIT",
    "DELAY": "EXIT",
    "SKIP": "EXIT",
    "GOTO": "EXIT",
    "LABEL": "EXIT",
    "JUMP": "EXIT",
    "RUN": "EXIT",

    # Functions
    "FUNC": "FUNC",
    "FUNCTION": "FUNC",
    "PARAM": "FUNC",
    "ARG": "FUNC",
    "CALLFUNC": "FUNC",
    "INLINE": "FUNC",
    "LAMBDA": "FUNC",
    "RECURSE": "FUNC",
    "OVERLOAD": "FUNC",
    "EXTEND": "FUNC",
    "WRAP": "FUNC",
    "HOOK": "FUNC",
    "EVENT": "FUNC",
    "TRIGGER": "FUNC",
    "LISTEN": "FUNC",
    "ASYNC": "FUNC",
    "SYNC": "FUNC",
    "THREAD": "FUNC",
    "PROCESS": "FUNC",

    # Arrays
    "ARRAY": "OUT",
    "LIST": "OUT",
    "PUSH": "OUT",
    "POP": "OUT",
    "ADDSET": "OUT",
    "REMOVESET": "OUT",
    "INSERT": "OUT",
    "DELETEAT": "OUT",
    "GETAT": "OUT",
    "SETAT": "OUT",
    "FIRST": "OUT",
    "LAST": "OUT",
    "SIZE": "OUT",
    "LENGTH": "OUT",
    "SORT": "OUT",
    "REVERSE": "OUT",
    "FILTER": "OUT",
    "MAP": "OUT",
    "MERGE": "OUT",
    "SPLIT": "OUT",

    # Strings
    "TEXT": "OUT",
    "CHAR": "OUT",
    "STR": "OUT",
    "JOIN": "OUT",
    "CUT": "OUT",
    "SLICE": "OUT",
    "REPLACE": "OUT",
    "SEARCH": "OUT",
    "FINDSTR": "OUT",
    "MATCHSTR": "OUT",
    "UPPER": "OUT",
    "LOWER": "OUT",
    "TRIM": "OUT",
    "SPACE": "OUT",
    "FORMAT": "OUT",
    "CONCAT": "OUT",
    "PARSE": "OUT",
    "ENCODE": "OUT",
    "DECODE": "OUT",
    "COUNTCHAR": "OUT",

    # Type helpers
    "TYPE": "OUT",
    "CAST": "OUT",
    "INT": "OUT",
    "FLOAT": "OUT",
    "BOOL": "OUT",
    "STRINGIFY": "OUT",
    "NUMBER": "OUT",
    "DATE": "OUT",
    "TIME": "OUT",
    "OBJECT": "OUT",
    "CLASS": "OUT",
    "INSTANCE": "OUT",
    "NULL": "OUT",
    "EMPTY": "OUT",
    "VALID": "OUT",
    "INVALID": "OUT",
    "CONVERT": "OUT",
    "FORMATTYPE": "OUT",
    "DEFAULT": "OUT",
    "AUTO": "OUT",
}

KEYWORDS = CANONICAL_KEYWORDS | set(KEYWORD_ALIASES.keys()) | set(KEYWORD_ALIASES.values())


def normalize_keyword(keyword):
    return KEYWORD_ALIASES.get(keyword.upper(), keyword.upper())


# =====================================
# Symbols
# =====================================

SYMBOLS = {

    "+",
    "-",
    "*",
    "/",
    "%",
    "=",

    "==",
    "!=",

    "<",
    "<=",

    ">",
    ">=",

    "(",
    ")",

    "{",
    "}",

    "[",
    "]",

    ",",
    ".",
    ":"
}

"""
ZeroOne Compiler

errors.py

Version 2.0.0
"""


class ZeroOneError(Exception):
    """
    Base class of all ZeroOne errors.
    """

    def __init__(
        self,
        message
    ):

        super().__init__(
            message
        )


# =====================================
# Lexer
# =====================================

class LexerError(
    ZeroOneError
):

    def __init__(
        self,
        message
    ):

        super().__init__(
            message
        )


# =====================================
# Parser
# =====================================

class ParserError(
    ZeroOneError
):

    def __init__(
        self,
        message
    ):

        super().__init__(
            message
        )


# =====================================
# Generator
# =====================================

class GeneratorError(
    ZeroOneError
):

    def __init__(
        self,
        message
    ):

        super().__init__(
            message
        )


# =====================================
# Assembler
# =====================================

class AssemblerError(
    ZeroOneError
):

    def __init__(
        self,
        message
    ):

        super().__init__(
            message
        )


# =====================================
# ByteCode
# =====================================

class ByteCodeError(
    ZeroOneError
):

    def __init__(
        self,
        message
    ):

        super().__init__(
            message
        )


# =====================================
# Virtual Machine
# =====================================

class VMError(
    ZeroOneError
):

    def __init__(
        self,
        message
    ):

        super().__init__(
            message
        )


# =====================================
# Compiler
# =====================================

class CompilerError(
    ZeroOneError
):

    def __init__(
        self,
        message
    ):

        super().__init__(
            message
        )


# =====================================
# Runtime
# =====================================

class RuntimeError(
    ZeroOneError
):

    def __init__(
        self,
        message
    ):

        super().__init__(
            message
        )


# =====================================
# Internal
# =====================================

class InternalCompilerError(
    ZeroOneError
):

    def __init__(
        self,
        message="Internal compiler error."
    ):

        super().__init__(
            message
        )

"""
ZeroOne Compiler

ast.py

Version 2.0.0
"""


# =====================================
# Base
# =====================================

class ASTNode:
    """
    Base class of all AST nodes.
    """
    pass


# =====================================
# Program
# =====================================

class ProgramNode(ASTNode):

    def __init__(self, statements=None):

        if statements is None:
            statements = []

        self.statements = statements

    def add(self, statement):
        self.statements.append(statement)


# =====================================
# Literal
# =====================================

class NumberNode(ASTNode):

    def __init__(self, value):
        self.value = value


class StringNode(ASTNode):

    def __init__(self, value):
        self.value = value


class BooleanNode(ASTNode):

    def __init__(self, value):
        self.value = bool(value)


class IdentifierNode(ASTNode):

    def __init__(self, name):
        self.name = name


# =====================================
# Expression
# =====================================

class BinaryOperationNode(ASTNode):

    def __init__(
        self,
        left,
        operator,
        right
    ):

        self.left = left
        self.operator = operator
        self.right = right


class UnaryOperationNode(ASTNode):

    def __init__(
        self,
        operator,
        value
    ):

        self.operator = operator
        self.value = value


class FunctionCallNode(ASTNode):

    def __init__(
        self,
        name,
        arguments
    ):

        self.name = name
        self.arguments = arguments


# =====================================
# Statement
# =====================================

class SetNode(ASTNode):

    def __init__(
        self,
        name,
        value
    ):

        self.name = name
        self.value = value


class OutNode(ASTNode):

    def __init__(
        self,
        value
    ):

        self.value = value


class ReturnNode(ASTNode):

    def __init__(
        self,
        value
    ):

        self.value = value


class ExitNode(ASTNode):
    pass


class ImportNode(ASTNode):

    def __init__(
        self,
        filename
    ):

        self.filename = filename


class AssetNode(ASTNode):

    def __init__(
        self,
        filename
    ):

        self.filename = filename


# =====================================
# Control
# =====================================

class WhenNode(ASTNode):

    def __init__(
        self,
        condition,
        body,
        else_body=None
    ):

        self.condition = condition
        self.body = body

        if else_body is None:
            else_body = []

        self.else_body = else_body


class LoopNode(ASTNode):

    def __init__(
        self,
        count,
        body
    ):

        self.count = count
        self.body = body


class BreakNode(ASTNode):
    pass


class ContinueNode(ASTNode):
    pass


# =====================================
# Function
# =====================================

class FunctionNode(ASTNode):

    def __init__(
        self,
        name,
        parameters,
        body
    ):

        self.name = name
        self.parameters = parameters
        self.body = body


# =====================================
# Future
# =====================================

class ArrayNode(ASTNode):

    def __init__(
        self,
        elements
    ):

        self.elements = elements


class IndexNode(ASTNode):

    def __init__(
        self,
        target,
        index
    ):

        self.target = target
        self.index = index


class PropertyNode(ASTNode):

    def __init__(
        self,
        target,
        name
    ):

        self.target = target
        self.name = name

"""
ZeroOne Compiler

opcode.py

Version 2.0.0
"""


class OpCode:

    # =====================================
    # Stack
    # =====================================

    PUSH = 1
    POP = 2
    DUP = 3
    SWAP = 4


    # =====================================
    # Memory
    # =====================================

    STORE = 10
    LOAD = 11


    # =====================================
    # Arithmetic
    # =====================================

    ADD = 20
    SUB = 21
    MUL = 22
    DIV = 23
    MOD = 24

    NEG = 25


    # =====================================
    # Compare
    # =====================================

    EQ = 30
    NE = 31
    LT = 32
    LE = 33
    GT = 34
    GE = 35


    # =====================================
    # Logic
    # =====================================

    AND = 40
    OR = 41
    NOT = 42


    # =====================================
    # Jump
    # =====================================

    JMP = 50

    JMP_IF_TRUE = 51

    JMP_IF_FALSE = 52

    LABEL = 53


    # =====================================
    # Function
    # =====================================

    CALL = 60

    RETURN = 61


    # =====================================
    # Output
    # =====================================

    PRINT = 70


    # =====================================
    # Array (Future)
    # =====================================

    ARRAY_NEW = 80

    ARRAY_GET = 81

    ARRAY_SET = 82

    ARRAY_LENGTH = 83


    # =====================================
    # Object (Future)
    # =====================================

    LOAD_PROPERTY = 90

    STORE_PROPERTY = 91


    # =====================================
    # System
    # =====================================

    EXIT = 255


    # =====================================
    # Debug
    # =====================================

    @staticmethod
    def name(code):

        table = {

            # Stack
            OpCode.PUSH:"PUSH",
            OpCode.POP:"POP",
            OpCode.DUP:"DUP",
            OpCode.SWAP:"SWAP",

            # Memory
            OpCode.STORE:"STORE",
            OpCode.LOAD:"LOAD",

            # Arithmetic
            OpCode.ADD:"ADD",
            OpCode.SUB:"SUB",
            OpCode.MUL:"MUL",
            OpCode.DIV:"DIV",
            OpCode.MOD:"MOD",
            OpCode.NEG:"NEG",

            # Compare
            OpCode.EQ:"EQ",
            OpCode.NE:"NE",
            OpCode.LT:"LT",
            OpCode.LE:"LE",
            OpCode.GT:"GT",
            OpCode.GE:"GE",

            # Logic
            OpCode.AND:"AND",
            OpCode.OR:"OR",
            OpCode.NOT:"NOT",

            # Jump
            OpCode.JMP:"JMP",
            OpCode.JMP_IF_TRUE:"JMP_IF_TRUE",
            OpCode.JMP_IF_FALSE:"JMP_IF_FALSE",
            OpCode.LABEL:"LABEL",

            # Function
            OpCode.CALL:"CALL",
            OpCode.RETURN:"RETURN",

            # Output
            OpCode.PRINT:"PRINT",

            # Array
            OpCode.ARRAY_NEW:"ARRAY_NEW",
            OpCode.ARRAY_GET:"ARRAY_GET",
            OpCode.ARRAY_SET:"ARRAY_SET",
            OpCode.ARRAY_LENGTH:"ARRAY_LENGTH",

            # Object
            OpCode.LOAD_PROPERTY:"LOAD_PROPERTY",
            OpCode.STORE_PROPERTY:"STORE_PROPERTY",

            # System
            OpCode.EXIT:"EXIT"

        }

        return table.get(
            code,
            "UNKNOWN"
        )

