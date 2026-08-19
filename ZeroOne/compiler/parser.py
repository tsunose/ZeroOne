"""
ZeroOne Compiler

parser.py

Version 2.0.0
"""

from compiler.tokens import TokenType, normalize_keyword
from compiler.ast import *
from compiler.errors import ParserError


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens

        self.position = 0

        self.current = (
            tokens[0]
            if tokens
            else None
        )

    # =====================================
    # Utility
    # =====================================

    def advance(self):

        self.position += 1

        if self.position < len(self.tokens):

            self.current = self.tokens[
                self.position
            ]

        else:

            self.current = None


    def peek(self):

        index = self.position + 1

        if index >= len(self.tokens):

            return None

        return self.tokens[index]


    def check(
        self,
        token_type
    ):

        return (

            self.current is not None

            and

            self.current.type == token_type

        )


    def check_keyword(
        self,
        keyword
    ):

        return (

            self.current is not None

            and

            self.current.type == TokenType.KEYWORD

            and

            normalize_keyword(self.current.value)
            ==
            normalize_keyword(keyword)

        )


    def match(
        self,
        token_type
    ):

        if self.check(token_type):

            token = self.current

            self.advance()

            return token

        return None


    def match_keyword(
        self,
        keyword
    ):

        if self.check_keyword(keyword):

            token = self.current

            self.advance()

            return token

        return None


    def expect(
        self,
        token_type
    ):

        token = self.match(
            token_type
        )

        if token is None:

            raise ParserError(

                f"Expected "

                f"{token_type.name}"

            )

        return token


    def expect_keyword(
        self,
        keyword
    ):

        token = self.match_keyword(
            keyword
        )

        if token is None:

            raise ParserError(

                f"Expected keyword "

                f"{keyword}"

            )

        return token


    def skip_newline(self):

        while self.check(
            TokenType.NEWLINE
        ):

            self.advance()


    def is_end(self):

        return (

            self.current is None

            or

            self.check(
                TokenType.EOF
            )

        )

    # =====================================
    # Entry
    # =====================================

    def parse(self):

        program = ProgramNode()

        self.skip_newline()

        while not self.is_end():

            node = self.parse_statement()

            if node is not None:

                program.add(node)

            self.skip_newline()

        return program

    # =====================================
    # Statement Dispatcher
    # =====================================

    def parse_statement(self):

        if self.check_keyword("SET"):
            return self.parse_set()

        if self.check_keyword("OUT"):
            return self.parse_out()

        if self.check_keyword("RETURN"):
            return self.parse_return()

        if self.check_keyword("EXIT"):
            return self.parse_exit()

        if self.check_keyword("IMPORT"):
            return self.parse_import()

        if self.check_keyword("ASSET"):
            return self.parse_asset()

        if self.check_keyword("WHEN"):
            return self.parse_when()

        if self.check_keyword("LOOP"):
            return self.parse_loop()

        if self.check_keyword("FUNC"):
            return self.parse_function()

        if self.check(TokenType.IDENTIFIER):
            return self.parse_index_assignment()

        if (
            self.current is not None
            and
            self.current.type == TokenType.KEYWORD
        ):
            self.advance()
            return NoOpNode()

        raise ParserError(

            f"Unexpected token "

            f"{self.current}"

        )

    # =====================================
    # SET
    # =====================================

    def parse_set(self):

        self.expect_keyword(
            "SET"
        )

        name = self.expect(
            TokenType.IDENTIFIER
        ).value

        value = self.parse_expression()

        return SetNode(
            name,
            value
        )


    # =====================================
    # OUT
    # =====================================

    def parse_out(self):

        self.expect_keyword(
            "OUT"
        )

        if self.is_end() or self.check(TokenType.NEWLINE) or self.check(TokenType.EOF):
            return OutNode(None)

        value = self.parse_expression()

        return OutNode(
            value
        )


    # =====================================
    # RETURN
    # =====================================

    def parse_return(self):

        self.expect_keyword(
            "RETURN"
        )

        value = self.parse_expression()

        return ReturnNode(
            value
        )


    # =====================================
    # EXIT
    # =====================================

    def parse_exit(self):

        self.expect_keyword(
            "EXIT"
        )

        return ExitNode()


    # =====================================
    # IMPORT
    # =====================================

    def parse_import(self):

        self.expect_keyword(
            "IMPORT"
        )

        filename = self.expect(
            TokenType.STRING
        ).value

        return ImportNode(
            filename
        )


    # =====================================
    # ASSET
    # =====================================

    def parse_asset(self):

        self.expect_keyword(
            "ASSET"
        )

        filename = self.expect(
            TokenType.STRING
        ).value

        return AssetNode(
            filename
        )

    # =====================================
    # INDEX ASSIGNMENT (arr[index] = value)
    # =====================================

    def parse_index_assignment(self):

        name = self.expect(
            TokenType.IDENTIFIER
        ).value

        target = IdentifierNode(name)

        if not (
            self.check(TokenType.SYMBOL)
            and
            self.current.value == "["
        ):

            raise ParserError(
                "Expected '[' after identifier "
                "in statement"
            )

        self.advance()

        index_expr = self.parse_expression()

        if (
            not self.check(TokenType.SYMBOL)
            or
            self.current.value != "]"
        ):

            raise ParserError(
                "Expected ']'"
            )

        self.advance()

        if (
            not self.check(TokenType.SYMBOL)
            or
            self.current.value != "="
        ):

            raise ParserError(
                "Expected '=' in index assignment"
            )

        self.advance()

        value = self.parse_expression()

        return IndexSetNode(
            target,
            index_expr,
            value
        )

    # ==========================
    # WHEN
    # ==========================

    def parse_when(self):

        self.expect_keyword("WHEN")

        condition = self.parse_expression()

        self.skip_newline()

        body = []

        else_body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("ELSE"):

                self.advance()

                self.skip_newline()

                while not self.is_end():

                    self.skip_newline()

                    if self.check_keyword("END"):

                        self.advance()

                        return WhenNode(
                            condition,
                            body,
                            else_body
                        )

                    else_body.append(
                        self.parse_statement()
                    )

                    self.skip_newline()

            if self.check_keyword("END"):

                self.advance()

                return WhenNode(
                    condition,
                    body,
                    else_body
                )

            body.append(
                self.parse_statement()
            )

            self.skip_newline()

        raise ParserError(
            "WHEN block missing END"
        )

    # ==========================
    # LOOP
    # ==========================

    def parse_loop(self):

        self.expect_keyword("LOOP")

        count = self.parse_expression()

        self.skip_newline()

        body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("END"):

                self.advance()

                return LoopNode(
                    count,
                    body
                )

            body.append(
                self.parse_statement()
            )

            self.skip_newline()

        raise ParserError(
            "LOOP block missing END"
        )

    # ==========================
    # FUNCTION
    # ==========================

    def parse_function(self):

        self.expect_keyword("FUNC")

        name = self.expect(
            TokenType.IDENTIFIER
        ).value

        params = []

        self.skip_newline()

        body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("END"):

                self.advance()

                return FunctionNode(
                    name,
                    params,
                    body
                )

            body.append(
                self.parse_statement()
            )

            self.skip_newline()

        raise ParserError(
            "FUNC block missing END"
        )

    # ==========================
    # Expression
    # ==========================

    def parse_expression(self):

        left = self.parse_primary()

        while (
            self.check(TokenType.SYMBOL)
            and
            self.current.value in (
                "+", "-", "*", "/", "%",
                "==", "!=", "<", "<=",
                ">", ">="
            )
        ):

            operator = self.current.value

            self.advance()

            right = self.parse_primary()

            left = BinaryOperationNode(
                left,
                operator,
                right
            )

        while self.check_keyword("AND"):

            self.advance()

            right = self.parse_primary()

            left = BinaryOperationNode(
                left,
                "AND",
                right
            )

        while self.check_keyword("OR"):

            self.advance()

            right = self.parse_primary()

            left = BinaryOperationNode(
                left,
                "OR",
                right
            )

        return left

    # ==========================
    # Primary
    # ==========================

    def parse_primary(self):

        if self.check(TokenType.NUMBER):

            value = int(
                self.current.value
            )

            self.advance()

            return NumberNode(value)

        if self.check(TokenType.STRING):

            value = self.current.value

            self.advance()

            return StringNode(value)

        if self.check_keyword("TRUE"):

            self.advance()

            return BooleanNode(True)

        if self.check_keyword("FALSE"):

            self.advance()

            return BooleanNode(False)

        if self.check(TokenType.IDENTIFIER):

            name = self.current.value

            self.advance()

            node = IdentifierNode(name)

            while (
                self.check(TokenType.SYMBOL)
                and
                self.current.value == "["
            ):

                self.advance()

                index_expr = self.parse_expression()

                if (
                    not self.check(TokenType.SYMBOL)
                    or
                    self.current.value != "]"
                ):

                    raise ParserError(
                        "Expected ']'"
                    )

                self.advance()

                node = IndexNode(
                    node,
                    index_expr
                )

            return node

        if self.check_keyword("NOT"):

            self.advance()

            value = self.parse_primary()

            return UnaryOperationNode(
                "NOT",
                value
            )

        if (
            self.check(TokenType.SYMBOL)
            and
            self.current.value == "("
        ):

            self.advance()

            expr = self.parse_expression()

            if (
                not self.check(TokenType.SYMBOL)
                or
                self.current.value != ")"
            ):

                raise ParserError(
                    "Expected ')'"
                )

            self.advance()

            return expr

        if (
            self.check(TokenType.SYMBOL)
            and
            self.current.value == "["
        ):

            self.advance()

            elements = []

            if not (
                self.check(TokenType.SYMBOL)
                and
                self.current.value == "]"
            ):

                elements.append(
                    self.parse_expression()
                )

                while (
                    self.check(TokenType.SYMBOL)
                    and
                    self.current.value == ","
                ):

                    self.advance()

                    elements.append(
                        self.parse_expression()
                    )

            if (
                not self.check(TokenType.SYMBOL)
                or
                self.current.value != "]"
            ):

                raise ParserError(
                    "Expected ']'"
                )

            self.advance()

            return ArrayNode(elements)

        raise ParserError(
            f"Unexpected token: {self.current}"
        )