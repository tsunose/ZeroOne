"""
ZeroOne Compiler

lexer.py

Version 2.0.2
"""

from compiler.tokens import (
    Token,
    TokenType,
    KEYWORDS,
    SYMBOLS,
    normalize_keyword,
)

from compiler.errors import LexerError


class Lexer:

    def __init__(
        self,
        text
    ):

        self.text = text

        self.position = 0

        self.line = 1

        self.column = 1


    # =====================================
    # Character
    # =====================================

    def current_char(self):

        if self.position >= len(self.text):

            return None

        return self.text[self.position]


    def peek(self):

        if self.position + 1 >= len(self.text):

            return None

        return self.text[
            self.position + 1
        ]


    def advance(self):

        ch = self.current_char()

        self.position += 1

        if ch == "\n":

            self.line += 1

            self.column = 1

        else:

            self.column += 1


    # =====================================
    # Skip
    # =====================================

    def skip_whitespace(self):

        while self.current_char() in (
            " ",
            "\t",
            "\r"
        ):

            self.advance()


    def skip_comment(self):

        while (
            self.current_char() is not None
            and
            self.current_char() != "\n"
        ):

            self.advance()


    # =====================================
    # Identifier
    # =====================================

    def read_identifier(self):

        start = self.column

        text = ""

        while (

            self.current_char() is not None

            and

            (

                self.current_char().isalnum()

                or

                self.current_char() == "_"

            )

        ):

            text += self.current_char()

            self.advance()


        upper = text.upper()


        if upper in KEYWORDS:

            # Keep the original keyword so aliases can be distinguished
            # by the compiler while check_keyword() still normalizes them.
            return Token(

                TokenType.KEYWORD,

                upper,

                self.line,

                start

            )


        return Token(

            TokenType.IDENTIFIER,

            text,

            self.line,

            start

        )


    # =====================================
    # Number
    # =====================================

    def read_number(self):

        start = self.column

        text = ""

        dot = False


        while self.current_char() is not None:


            ch = self.current_char()


            if ch == ".":

                if dot:

                    break

                dot = True

                text += ch

                self.advance()

                continue


            if not ch.isdigit():

                break


            text += ch

            self.advance()


        if dot:

            value = float(text)

        else:

            value = int(text)


        return Token(

            TokenType.NUMBER,

            value,

            self.line,

            start

        )


    # =====================================
    # String
    # =====================================

    def read_string(self):

        start = self.column

        self.advance()

        text = ""


        while True:


            ch = self.current_char()


            if ch is None:

                raise LexerError(

                    f"Unterminated string "

                    f"({self.line}:{start})"

                )


            if ch == "\"":

                break


            if ch == "\\":

                self.advance()

                ch = self.current_char()

                escapes = {

                    "n":"\n",

                    "t":"\t",

                    "r":"\r",

                    "\"":"\"",

                    "\\":"\\"

                }

                text += escapes.get(ch, ch)

                self.advance()

                continue


            text += ch

            self.advance()


        self.advance()


        return Token(

            TokenType.STRING,

            text,

            self.line,

            start

        )

    # =====================================
    # Symbol
    # =====================================

    def read_symbol(self):

        start = self.column

        ch = self.current_char()

        self.advance()

        # Longest-match symbol scanning.
        candidates = sorted(
            (sym for sym in SYMBOLS if sym.startswith(ch)),
            key=len, reverse=True
        )
        symbol = ch
        for candidate in candidates:
            if self.text.startswith(candidate, self.position - 1):
                symbol = candidate
                while self.position < len(self.text) and len(symbol) > 1 and self.text[self.position] == symbol[len(symbol)-1]:
                    # handled below by exact length advance
                    break
                extra = len(candidate) - 1
                for _ in range(extra):
                    self.advance()
                break

        if symbol not in SYMBOLS:

            raise LexerError(

                f"Unknown symbol '{symbol}' "

                f"({self.line}:{start})"

            )

        return Token(

            TokenType.SYMBOL,

            symbol,

            self.line,

            start

        )


    # =====================================
    # Tokenize
    # =====================================

    def tokenize(self):

        tokens = []

        while self.current_char() is not None:

            ch = self.current_char()

            # -----------------
            # Space
            # -----------------

            if ch in (" ", "\t", "\r"):

                self.skip_whitespace()

                continue

            # -----------------
            # New Line
            # -----------------

            if ch == "\n":

                tokens.append(

                    Token(

                        TokenType.NEWLINE,

                        "\\n",

                        self.line,

                        self.column

                    )

                )

                self.advance()

                continue

            # -----------------
            # Comment
            # -----------------

            if (
                ch == "/"
                and
                self.peek() == "/"
            ):

                self.skip_comment()

                continue

            # -----------------
            # String
            # -----------------

            if ch == "\"":

                tokens.append(

                    self.read_string()

                )

                continue

            # -----------------
            # Number
            # -----------------

            if ch.isdigit():

                tokens.append(

                    self.read_number()

                )

                continue

            # -----------------
            # Identifier
            # -----------------

            if (
                ch.isalpha()
                or
                ch == "_"
            ):

                tokens.append(

                    self.read_identifier()

                )

                continue

            # -----------------
            # Symbol
            # -----------------

            if ch in "+-*/%=<>!&|^~(){}[],:;?.":

                tokens.append(

                    self.read_symbol()

                )

                continue

            # -----------------
            # Error
            # -----------------

            raise LexerError(

                f"Unexpected character "

                f"'{ch}' "

                f"({self.line}:{self.column})"

            )

        # EOF

        tokens.append(

            Token(

                TokenType.EOF,

                "EOF",

                self.line,

                self.column

            )

        )

        return tokens