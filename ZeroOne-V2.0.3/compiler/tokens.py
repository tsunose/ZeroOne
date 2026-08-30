"""
ZeroOne Compiler

tokens.py

Version 2.0.3 - Extended Keywords
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
    "LET",
    "CONST",
    "VAR",

    # Output
    "OUT",

    # Input
    "IN",

    # Condition
    "WHEN",
    "ELSE",
    "END",
    "CASE",
    "DEFAULT",
    "SWITCH",

    # Loop
    "LOOP",
    "BREAK",
    "CONTINUE",
    "WHILE",
    "FOR",
    "FOREACH",

    # Function
    "FUNC",
    "RETURN",
    "LAMBDA",
    "ASYNC",
    "AWAIT",

    # Class/Object
    "CLASS",
    "EXTENDS",
    "NEW",
    "THIS",
    "SUPER",
    "STATIC",

    # Exception
    "TRY",
    "CATCH",
    "FINALLY",
    "THROW",

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

    # Type
    "TYPE",
    "CAST",
    "NULL",
    "VOID",

    # Math
    "MATH",

    # String
    "STRING",

    # Array
    "ARRAY",

    # Map/Object
    "MAP",
    "OBJECT",
}

KEYWORD_ALIASES = {
    # ===== Output/Display =====
    "PRINT": "OUT",
    "SHOW": "OUT",
    "VIEW": "OUT",
    "DISPLAY": "OUT",
    "ECHO": "OUT",
    "WRITE": "OUT",
    "PUT": "OUT",
    "DRAW": "OUT",
    "RENDER": "OUT",
    "ALERT": "OUT",
    "NOTICE": "OUT",
    "MSG": "OUT",
    "LOG": "OUT",
    "DEBUG": "OUT",
    "TRACE": "OUT",
    "DUMP": "OUT",
    "EXPORT": "OUT",
    "SEND": "OUT",

    # ===== Input =====
    "INPUT": "IN",
    "READ": "IN",
    "GET": "IN",
    "FETCH": "IN",
    "SCAN": "IN",
    "ASK": "IN",
    "QUERY": "IN",
    "RECEIVE": "IN",
    "LOAD": "IN",
    "OPEN": "IN",
    "SELECT": "IN",
    "CHOOSE": "IN",
    "PICK": "IN",
    "FIND": "IN",
    "SEARCH": "IN",
    "LOOK": "IN",
    "CHECK": "IN",
    "CAPTURE": "IN",

    # ===== Variables =====
    "DEFINE": "SET",
    "CREATE": "SET",
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

    # ===== Flow control =====
    "IF": "WHEN",
    "THEN": "WHEN",
    "EQ": "WHEN",
    "NE": "WHEN",
    "GT": "WHEN",
    "LT": "WHEN",
    "GE": "WHEN",
    "LE": "WHEN",

    # ===== Loop variants =====
    "UNTIL": "LOOP",
    "REPEAT": "LOOP",
    "DO": "LOOP",

    # ===== Functions =====
    "FUNCTION": "FUNC",
    "PARAM": "FUNC",
    "ARG": "FUNC",
    "CALLFUNC": "FUNC",
    "INLINE": "FUNC",
    "RECURSE": "FUNC",
    "OVERLOAD": "FUNC",
    "EXTEND": "FUNC",
    "WRAP": "FUNC",
    "HOOK": "FUNC",
    "EVENT": "FUNC",
    "TRIGGER": "FUNC",
    "LISTEN": "FUNC",
    "SYNC": "FUNC",
    "THREAD": "FUNC",
    "PROCESS": "FUNC",
    "YIELD": "FUNC",

    # ===== Math Operations =====
    "ADD": "MATH",
    "SUB": "MATH",
    "MUL": "MATH",
    "DIV": "MATH",
    "MOD": "MATH",
    "INC": "MATH",
    "DEC": "MATH",
    "POWER": "MATH",
    "ROOT": "MATH",
    "SQRT": "MATH",
    "ABS": "MATH",
    "ROUND": "MATH",
    "FLOOR": "MATH",
    "CEIL": "MATH",
    "TRUNC": "MATH",
    "MAX": "MATH",
    "MIN": "MATH",
    "AVG": "MATH",
    "SUM": "MATH",
    "COUNT": "MATH",
    "RANDOM": "MATH",
    "CLAMP": "MATH",
    "SIGN": "MATH",
    "EXP": "MATH",
    "LN": "MATH",
    "LOG": "MATH",
    "LOG10": "MATH",
    "SIN": "MATH",
    "COS": "MATH",
    "TAN": "MATH",
    "ASIN": "MATH",
    "ACOS": "MATH",
    "ATAN": "MATH",

    # ===== String Operations =====
    "TEXT": "STRING",
    "CHAR": "STRING",
    "STR": "STRING",
    "JOIN": "STRING",
    "CUT": "STRING",
    "SLICE": "STRING",
    "SUBSTR": "STRING",
    "REPLACE": "STRING",
    "UPPER": "STRING",
    "LOWER": "STRING",
    "TRIM": "STRING",
    "SPACE": "STRING",
    "FORMAT": "STRING",
    "CONCAT": "STRING",
    "PARSE": "STRING",
    "ENCODE": "STRING",
    "DECODE": "STRING",
    "COUNTCHAR": "STRING",
    "STARTSWITH": "STRING",
    "ENDSWITH": "STRING",
    "CONTAINS": "STRING",
    "REVERSE": "STRING",
    "REPEAT": "STRING",
    "SPLIT": "STRING",
    "FINDSTR": "STRING",
    "MATCHSTR": "STRING",
    "TOSTRING": "STRING",

    # ===== Array Operations =====
    "LIST": "ARRAY",
    "PUSH": "ARRAY",
    "POP": "ARRAY",
    "ADDSET": "ARRAY",
    "REMOVESET": "ARRAY",
    "INSERT": "ARRAY",
    "DELETEAT": "ARRAY",
    "GETAT": "ARRAY",
    "SETAT": "ARRAY",
    "FIRST": "ARRAY",
    "LAST": "ARRAY",
    "SIZE": "ARRAY",
    "LENGTH": "ARRAY",
    "SORT": "ARRAY",
    "REVERSE": "ARRAY",
    "FILTER": "ARRAY",
    "MAP": "ARRAY",
    "REDUCE": "ARRAY",
    "FOREACH": "ARRAY",
    "MERGE": "ARRAY",
    "SPLIT": "ARRAY",
    "FLATTEN": "ARRAY",
    "FLAT": "ARRAY",
    "UNIQUE": "ARRAY",
    "FIND": "ARRAY",
    "FINDINDEX": "ARRAY",
    "INCLUDES": "ARRAY",
    "INDEXOF": "ARRAY",
    "SHIFT": "ARRAY",
    "UNSHIFT": "ARRAY",
    "SLICE": "ARRAY",
    "SPLICE": "ARRAY",
    "CONCAT": "ARRAY",
    "FILL": "ARRAY",
    "COPY": "ARRAY",

    # ===== Map/Object Operations =====
    "KEYS": "MAP",
    "VALUES": "MAP",
    "ENTRIES": "MAP",
    "HAS": "MAP",
    "CLEAR": "MAP",
    "MERGE": "MAP",
    "PROPERTY": "MAP",
    "PROP": "MAP",

    # ===== Type Operations =====
    "TYPE_OF": "TYPE",
    "TYPEOF": "TYPE",
    "IS": "TYPE",
    "AS": "CAST",
    "INT": "CAST",
    "FLOAT": "CAST",
    "BOOL": "CAST",
    "STRINGIFY": "CAST",
    "NUMBER": "CAST",
    "DATE": "CAST",
    "TIME": "CAST",
    "INSTANCE": "TYPE",
    "EMPTY": "TYPE",
    "VALID": "TYPE",
    "INVALID": "TYPE",
    "CONVERT": "TYPE",
    "FORMATTYPE": "TYPE",
    "DEFAULT": "TYPE",
    "AUTO": "TYPE",

    # ===== File I/O =====
    "FILE": "IN",
    "FILE_READ": "IN",
    "FILE_WRITE": "WRITE",
    "FILE_APPEND": "WRITE",
    "FILE_EXISTS": "IN",
    "FILE_SIZE": "IN",
    "FILE_DELETE": "DELETE",
    "FILE_COPY": "COPY",
    "FILE_MOVE": "MOVE",
    "DIR_CREATE": "CREATE",
    "DIR_EXISTS": "CHECK",
    "DIR_LIST": "READ",
    "DIR_DELETE": "DELETE",
    "PATH": "IN",

    # ===== System Operations =====
    "SYSTEMOS": "OUT",
    "SYSTEM": "OUT",
    "ENV": "IN",
    "ARGV": "IN",
    "GETPID": "IN",
    "SLEEP": "OUT",
    "TIME": "IN",
    "TIMESTAMP": "IN",
    "SEED": "MATH",
    "VERSION": "OUT",

    # ===== Security/Hash =====
    "SECURE": "OUT",
    "HASH": "OUT",
    "MD5": "OUT",
    "SHA": "OUT",
    "SHA1": "OUT",
    "SHA256": "OUT",
    "SHA512": "OUT",
    "BASE64": "OUT",
    "ENCODE64": "ENCODE",
    "DECODE64": "DECODE",
    "HEX": "OUT",

    # ===== Data/JSON =====
    "DATA": "OUT",
    "TABLE": "ARRAY",
    "ROW": "ARRAY",
    "COLUMN": "ARRAY",
    "CELL": "ARRAY",
    "JSON": "OUT",
    "YAML": "OUT",
    "PARSE_JSON": "PARSE",
    "STRINGIFY_JSON": "PARSE",

    # ===== Logic Gates =====
    "XOR": "AND",
    "NAND": "AND",
    "NOR": "OR",

    # ===== Advanced =====
    "GENERATOR": "FUNC",
    "NEXT": "FUNC",
    "ITERATOR": "FUNC",
    "ENUM": "TYPE",
    "STRUCT": "TYPE",
    "UNION": "TYPE",
    "REGEX": "STRING",
    "PATTERN": "STRING",
    "MATCH": "STRING",
    "DESTRUCTURE": "SET",
    "SPREAD": "SET",
    "REST": "SET",

    # ===== Promise/Callback =====
    "PROMISE": "FUNC",
    "THEN": "FUNC",
    "CATCH": "FUNC",
    "FINALLY": "FUNC",
}

# Only canonical syntax words are lexer-reserved. Legacy aliases/built-in names remain identifiers.
# so names such as add, size, sort, parse, format, etc. can be used as identifiers.
# A small set of legacy spellings are retained only because the parser
# treats them as grammar aliases (IF/FUNCTION/UNTIL/REPEAT/DO).
SYNTAX_ALIASES = {
    "IF": "WHEN",
    "THEN": "WHEN",
    "FUNCTION": "FUNC",
    "UNTIL": "LOOP",
    "REPEAT": "LOOP",
    "DO": "LOOP",
}

KEYWORDS = set(CANONICAL_KEYWORDS) | set(SYNTAX_ALIASES)


def normalize_keyword(keyword):
    upper = str(keyword).upper()
    return SYNTAX_ALIASES.get(upper, upper)


# =====================================
# Symbols
# =====================================

SYMBOLS = {
    # Arithmetic
    "+",
    "-",
    "*",
    "/",
    "%",
    "**",  # Power

    # Assignment
    "=",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "**=",

    # Comparison
    "==",
    "!=",
    "<",
    "<=",
    ">",
    ">=",
    "===",
    "!==",

    # Logical
    "&&",
    "||",
    "!",

    # Bitwise
    "&",
    "|",
    "^",
    "~",
    "<<",
    ">>",
    ">>>",

    # Brackets
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",

    # Delimiters
    ",",
    ".",
    ":",
    ";",
    "->",
    "=>",
    "...",  # Spread/Rest

    # Other
    "?",
    "@",
    "#",
    "$",
}
