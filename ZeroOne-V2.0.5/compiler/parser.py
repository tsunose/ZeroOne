"""
ZeroOne Compiler

parser.py

Version 2.0.4 - Extended Parser
"""

from compiler.tokens import TokenType, normalize_keyword, KEYWORD_ALIASES
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


    def peek_ahead(self, n=1):
        """n個先のトークンを確認"""

        index = self.position + n

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


    def check_symbol(self, symbol):
        """シンボルをチェック"""

        return (
            self.current is not None
            and
            self.current.type == TokenType.SYMBOL
            and
            self.current.value == symbol
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


    def match_symbol(self, symbol):
        """シンボルにマッチ"""

        if self.check_symbol(symbol):

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


    def expect_symbol(self, symbol):
        """シンボルを期待"""

        token = self.match_symbol(symbol)

        if token is None:

            raise ParserError(

                f"Expected symbol '{symbol}'"

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

        # Some extended keywords intentionally normalize to legacy command
        # categories (for compatibility). Give their original spelling first
        # chance so FILE_*, DIR_*, HASH/JSON/system operations are not reduced
        # to OUT/IN/SET.
        if self.current is not None and self.current.type == TokenType.KEYWORD:
            # Declarations have dedicated parsers; they must not fall through
            # to the generic built-in-call parser.
            if self.check_keyword("ENUM"):
                return self.parse_enum()
            if self.check_keyword("STRUCT"):
                return self.parse_struct()
            extended = {
                "FILE","FILE_READ","FILE_WRITE","FILE_APPEND","FILE_EXISTS","FILE_SIZE","FILE_DELETE","FILE_COPY","FILE_MOVE",
                "DIR_CREATE","DIR_EXISTS","DIR_LIST","DIR_DELETE","PATH",
                "SYSTEMOS","SYSTEM","ENV","ARGV","GETPID","GETPPID","SLEEP","TIMESTAMP","SEED","VERSION","PLATFORM","ARCH",
                "SECURE","HASH","MD5","SHA","SHA1","SHA256","SHA512","BASE64","ENCODE64","DECODE64","HEX",
                "DATA","TABLE","ROW","COLUMN","CELL","JSON","YAML","PARSE_JSON","STRINGIFY_JSON",
                "TYPE","CAST","TYPE_OF","TYPEOF","INT","FLOAT","BOOL","STRINGIFY","NUMBER","DATE","TIME","INSTANCE","EMPTY","VALID","INVALID","CONVERT","AUTO",
                "ADD","SUB","MUL","DIV","MOD","POWER","ROOT","SQRT","ABS","ROUND","FLOOR","CEIL","TRUNC","MAX","MIN","AVG","SUM","COUNT","RANDOM","CLAMP","SIGN","EXP","LN","LOG10","SIN","COS","TAN","ASIN","ACOS","ATAN",
                "STRING","TEXT","CHAR","STR","JOIN","CUT","SLICE","SUBSTR","REPLACE","UPPER","LOWER","TRIM","SPACE","FORMAT","CONCAT","PARSE","ENCODE","DECODE","COUNTCHAR","STARTSWITH","ENDSWITH","CONTAINS","REVERSE","SPLIT","FINDSTR","MATCHSTR","TOSTRING",
                "ARRAY","MAP","LIST","PUSH","POP","ADDSET","REMOVESET","INSERT","DELETEAT","GETAT","SETAT","FIRST","LAST","SIZE","LENGTH","SORT","FILTER","REDUCE","MERGE","FLATTEN","FLAT","UNIQUE","FIND","FINDINDEX","INCLUDES","INDEXOF","SHIFT","UNSHIFT","SPLICE","FILL","COPY",
                "KEYS","VALUES","ENTRIES","HAS","PROPERTY","PROP","REGEX","PATTERN","MATCH","UNION","GENERATOR","NEXT","ITERATOR","DESTRUCTURE","SPREAD","REST","PROMISE","ASYNC","AWAIT","ASSERT","DEBUG","WARN","ERROR","DUMP","DISASM","NOP","NOOP"
            }
            if self.current.value in extended:
                return self.parse_builtin_statement()

        # Variable assignment
        if self.check_keyword("SET") or self.check_keyword("LET") or self.check_keyword("CONST"):
            return self.parse_set()

        # Output
        if self.check_keyword("OUT"):
            return self.parse_out()

        # Input
        if self.check_keyword("IN"):
            return self.parse_input()

        # Return
        if self.check_keyword("RETURN"):
            return self.parse_return()

        # Exit
        if self.check_keyword("EXIT"):
            return self.parse_exit()

        # Import
        if self.check_keyword("IMPORT"):
            return self.parse_import()

        # Export
        if self.check_keyword("EXPORT"):
            return self.parse_export()

        # Asset
        if self.check_keyword("ASSET"):
            return self.parse_asset()

        # Control Flow
        if self.check_keyword("WHEN") or self.check_keyword("IF"):
            return self.parse_when()

        if self.check_keyword("SWITCH"):
            return self.parse_switch()

        # Loops
        if self.check_keyword("LOOP"):
            return self.parse_loop()

        if self.check_keyword("WHILE"):
            return self.parse_while()

        if self.check_keyword("FOR"):
            return self.parse_for()

        if self.check_keyword("FOREACH"):
            return self.parse_foreach()

        # Exception Handling
        if self.check_keyword("TRY"):
            return self.parse_try()

        if self.check_keyword("THROW"):
            return self.parse_throw()

        # Function Definition
        if self.check_keyword("FUNC"):
            return self.parse_function()

        # Class Definition
        if self.check_keyword("CLASS"):
            return self.parse_class()

        # Break/Continue
        if self.check_keyword("BREAK"):
            self.advance()
            return BreakNode()

        if self.check_keyword("CONTINUE"):
            self.advance()
            return ContinueNode()

        # Expression Statement or Array Index Assignment
        if self.check(TokenType.IDENTIFIER):
            return self.parse_identifier_statement()

        # All other reserved language commands are parsed as built-ins.
        # This is intentionally the final dispatcher so control-flow keywords
        # keep their dedicated grammar above.
        if self.current is not None and self.current.type == TokenType.KEYWORD:
            return self.parse_builtin_statement()

        raise ParserError(

            f"Unexpected token "

            f"{self.current}"

        )

    # =====================================
    # Built-in / reserved operations
    # =====================================

    def parse_builtin_statement(self):
        name = self.current.value
        self.advance()
        args = []

        # FUNCTION-LIKE form: OP(a, b, c)
        if self.check_symbol("("):
            self.advance()
            while not self.check_symbol(")"):
                args.append(self.parse_expression())
                if not self.check_symbol(")"):
                    self.expect_symbol(",")
            self.expect_symbol(")")
            return BuiltinCallNode(name, args)

        # Line form: OP a b. Expressions are separated by whitespace/newline.
        # Known operators get their natural arity; unknown reserved words are
        # still accepted and become a harmless runtime NOP.
        arity = {
            # Math / logic
            "ADD":2,"SUB":2,"MUL":2,"DIV":2,"MOD":2,"POWER":2,"MAX":2,"MIN":2,"CLAMP":3,
            "EQ":2,"NE":2,"LT":2,"LE":2,"GT":2,"GE":2,"AND":2,"OR":2,"XOR":2,"NAND":2,"NOR":2,"XNOR":2,
            "BITAND":2,"BITOR":2,"BITXOR":2,"LSHIFT":2,"RSHIFT":2,"ARSHIFT":2,"ROTL":2,"ROTR":2,
            "ABS":1,"SQRT":1,"EXP":1,"LN":1,"LOG":1,"LOG10":1,"SIN":1,"COS":1,"TAN":1,
            "ASIN":1,"ACOS":1,"ATAN":1,"FLOOR":1,"CEIL":1,"ROUND":1,"TRUNC":1,"SIGN":1,"FAC":1,
            "NOT":1,"BITNOT":1,"POPCOUNT":1,
            # Strings
            "CHAR":1,"STR":1,"TEXT":1,"TOSTRING":1,"UPPER":1,"LOWER":1,"TRIM":1,"REVERSE":1,
            "LENGTH":1,"SIZE":1,"FIRST":1,"LAST":1,"SPACE":1,"CUT":2,"SLICE":3,"SUBSTR":3,
            "REPLACE":3,"STARTSWITH":2,"ENDSWITH":2,"CONTAINS":2,"REPEAT":2,"SPLIT":2,"FINDSTR":2,"MATCHSTR":2,
            "COUNTCHAR":2,"JOIN":2,"CONCAT":2,"FORMAT":2,"ENCODE":2,"DECODE":2,
            # Arrays
            "LIST":0,"PUSH":2,"POP":1,"INSERT":3,"DELETEAT":2,"GETAT":2,"SETAT":3,"SHIFT":1,"UNSHIFT":2,
            "SORT":1,"FILTER":2,"REDUCE":3,"MERGE":2,"FLATTEN":1,"FLAT":1,"UNIQUE":1,"FIND":2,"FINDINDEX":2,
            "INCLUDES":2,"INDEXOF":2,"SPLICE":3,"FILL":3,"COPY":1,
            # Maps / types
            "KEYS":1,"VALUES":1,"ENTRIES":1,"HAS":2,"PROPERTY":2,"PROP":2,"TYPE_OF":1,"TYPEOF":1,
            "IS":2,"INT":1,"FLOAT":1,"BOOL":1,"STRINGIFY":1,"NUMBER":1,"INSTANCE":2,"EMPTY":1,"VALID":1,"INVALID":1,"CONVERT":2,"AUTO":1,
            # Files / system
            "FILE_READ":1,"FILE_WRITE":2,"FILE_APPEND":2,"FILE_EXISTS":1,"FILE_SIZE":1,"FILE_DELETE":1,"FILE_COPY":2,"FILE_MOVE":2,
            "DIR_CREATE":1,"DIR_EXISTS":1,"DIR_LIST":1,"DIR_DELETE":1,"PATH":0,"ENV":1,"ARGV":0,"GETPID":0,"GETPPID":0,
            "SLEEP":1,"TIMESTAMP":0,"SEED":1,"RANDOM":0,"VERSION":0,"SYSTEM":1,"SYSTEMOS":0,"PLATFORM":0,"ARCH":0,
            # Security / data
            "HASH":1,"MD5":1,"SHA":1,"SHA1":1,"SHA256":1,"SHA512":1,"BASE64":1,"ENCODE64":1,"DECODE64":1,"HEX":1,
            "JSON":1,"YAML":1,"PARSE_JSON":1,"STRINGIFY_JSON":1,
            # Advanced helpers
            "REGEX":1,"PATTERN":1,"MATCH":2,"NEXT":1,"ITERATOR":1,"GENERATOR":1,"DESTRUCTURE":2,"SPREAD":1,"REST":1,
            "PROMISE":1,"THEN":2,"ASYNC":1,"AWAIT":1,"ASSERT":2,"DEBUG":1,"WARN":1,"ERROR":1,"DUMP":1,"DISASM":1,
            "ENUM":2,"STRUCT":2,"UNION":2,"NOP":0,"NOOP":0,
            "INPUT":1,"IN":1,
        }.get(name)
        if arity is None:
            # Categories/canonical extension keywords accept zero or one value.
            arity = 1 if not (self.is_end() or self.check(TokenType.NEWLINE)) else 0

        for _ in range(arity):
            if self.is_end() or self.check(TokenType.NEWLINE) or self.check_symbol(")"):
                break
            args.append(self.parse_expression())
        return BuiltinCallNode(name, args)

    # =====================================
    # SET (Variable Assignment)
    # =====================================

    def parse_set(self):

        keyword = self.current.value
        self.advance()

        is_const = normalize_keyword(keyword) == "CONST"

        name = self.expect(
            TokenType.IDENTIFIER
        ).value

        # Property assignment: SET object.field = value
        if self.check_symbol("."):
            self.advance()
            if not (self.check(TokenType.IDENTIFIER) or self.check(TokenType.KEYWORD)):
                raise ParserError("Expected property name.")
            property_name = self.current.value
            self.advance()
            if self.check_symbol("="):
                self.advance()
            value = self.parse_expression()
            return PropertySetNode(IdentifierNode(name), property_name, value)

        # Both SET name = value and the original compact SET name value form
        # are accepted.
        if self.check_symbol("="):
            self.advance()

        value = self.parse_expression()

        return SetNode(
            name,
            value,
            is_const
        )


    # =====================================
    # OUT (Output)
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
    # IN (Input)
    # =====================================

    def parse_input(self):

        self.expect_keyword("IN")

        # IN is an expression-capable builtin.  A prompt is optional.
        args = []
        if not (self.is_end() or self.check(TokenType.NEWLINE) or self.check(TokenType.EOF)):
            args.append(self.parse_expression())
        return BuiltinCallNode("INPUT", args)


    # =====================================
    # RETURN
    # =====================================

    def parse_return(self):

        self.expect_keyword(
            "RETURN"
        )

        value = None
        if not (self.is_end() or self.check(TokenType.NEWLINE)):
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

        code = 0
        if not (self.is_end() or self.check(TokenType.NEWLINE)):
            expr = self.parse_expression()
            if isinstance(expr, NumberNode):
                code = expr.value

        return ExitNode(code)


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
    # ENUM / STRUCT declarations
    # =====================================

    def _expect_name(self):
        if self.check(TokenType.IDENTIFIER) or self.check(TokenType.KEYWORD):
            value = self.current.value
            self.advance()
            return value
        raise ParserError("Expected name.")

    def parse_enum(self):
        self.expect_keyword("ENUM")
        name = self._expect_name()
        members = []
        self.skip_newline()
        next_value = 0
        while not self.is_end() and not self.check_keyword("END"):
            if self.check(TokenType.NEWLINE):
                self.advance(); continue
            member = self._expect_name()
            value = next_value
            if self.check_symbol("="):
                self.advance()
                value_node = self.parse_expression()
                if isinstance(value_node, NumberNode):
                    value = value_node.value
                else:
                    raise ParserError("ENUM values must be numeric constants.")
            members.append((member, value))
            next_value = int(value) + 1
            self.skip_newline()
        self.expect_keyword("END")
        return EnumNode(name, members)

    def parse_struct(self):
        self.expect_keyword("STRUCT")
        name = self._expect_name()
        fields = []
        self.skip_newline()
        while not self.is_end() and not self.check_keyword("END"):
            if self.check(TokenType.NEWLINE):
                self.advance(); continue
            field = self._expect_name()
            fields.append((field, None))
            # Optional type annotation: `field TYPE`
            if not self.check(TokenType.NEWLINE) and not self.check_keyword("END"):
                if self.check(TokenType.IDENTIFIER) or self.check(TokenType.KEYWORD):
                    self.advance()
            self.skip_newline()
        self.expect_keyword("END")
        return StructNode(name, fields)

    # =====================================
    # EXPORT
    # =====================================

    def parse_export(self):
        self.expect_keyword("EXPORT")
        names = []
        while not self.is_end() and not self.check(TokenType.NEWLINE):
            if self.check_symbol(","):
                self.advance()
                continue
            names.append(self._expect_name())
        return ExportNode(names)

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
    # WHEN (If-Else)
    # =====================================

    def parse_when(self):

        self.expect_keyword("WHEN") if self.check_keyword("WHEN") else self.expect_keyword("IF")

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


    # =====================================
    # SWITCH (Case Statement)
    # =====================================

    def parse_switch(self):

        self.expect_keyword("SWITCH")

        expression = self.parse_expression()

        self.skip_newline()

        cases = []
        default_body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("CASE"):

                self.advance()

                value = self.parse_expression()

                self.expect_symbol(":")

                self.skip_newline()

                body = []

                while not self.is_end() and not self.check_keyword("CASE") and not self.check_keyword("DEFAULT") and not self.check_keyword("END"):

                    body.append(self.parse_statement())

                    self.skip_newline()

                cases.append(CaseNode(value, body))

            elif self.check_keyword("DEFAULT"):

                self.advance()

                self.expect_symbol(":")

                self.skip_newline()

                while not self.is_end() and not self.check_keyword("END"):

                    default_body.append(self.parse_statement())

                    self.skip_newline()

            elif self.check_keyword("END"):

                self.advance()

                return SwitchNode(expression, cases, default_body)

            else:

                raise ParserError("Expected CASE, DEFAULT, or END in SWITCH")

        raise ParserError("SWITCH block missing END")


    # =====================================
    # LOOP (Simple Loop)
    # =====================================

    def parse_loop(self):

        self.expect_keyword("LOOP")

        # LOOP by itself is a valid reserved command/no-op form.
        if self.check(TokenType.NEWLINE) or self.check(TokenType.EOF):
            return LoopNode(NumberNode(0), [])

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


    # =====================================
    # WHILE
    # =====================================

    def parse_while(self):

        self.expect_keyword("WHILE")

        condition = self.parse_expression()

        self.skip_newline()

        body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("END"):

                self.advance()

                return WhileNode(condition, body)

            body.append(self.parse_statement())

            self.skip_newline()

        raise ParserError("WHILE block missing END")


    # =====================================
    # FOR
    # =====================================

    def parse_for(self):

        self.expect_keyword("FOR")

        # FOR init; condition; update
        init = None
        if not self.check_symbol(";"):
            if self.check_keyword("SET") or self.check_keyword("LET") or self.check_keyword("CONST"):
                init = self.parse_set()
            else:
                init = self.parse_expression()

        self.expect_symbol(";")

        condition = None
        if not self.check_symbol(";"):
            condition = self.parse_expression()

        self.expect_symbol(";")

        update = None
        if not self.check_keyword("END") and not self.check(TokenType.NEWLINE):
            if self.check_keyword("SET") or self.check_keyword("LET") or self.check_keyword("CONST"):
                update = self.parse_set()
            else:
                update = self.parse_expression()

        self.skip_newline()

        body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("END"):

                self.advance()

                return ForNode(init, condition, update, body)

            body.append(self.parse_statement())

            self.skip_newline()

        raise ParserError("FOR block missing END")


    # =====================================
    # FOREACH
    # =====================================

    def parse_foreach(self):

        self.expect_keyword("FOREACH")

        variable = self.expect(TokenType.IDENTIFIER).value

        self.expect_keyword("IN")

        iterable = self.parse_expression()

        self.skip_newline()

        body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("END"):

                self.advance()

                return ForEachNode(variable, iterable, body)

            body.append(self.parse_statement())

            self.skip_newline()

        raise ParserError("FOREACH block missing END")


    # =====================================
    # TRY-CATCH-FINALLY
    # =====================================

    def parse_try(self):

        self.expect_keyword("TRY")

        self.skip_newline()

        try_body = []

        catch_clause = None
        finally_body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("CATCH"):

                self.advance()

                exception_type = "Exception"
                variable = "e"

                if self.check_symbol("("):
                    self.advance()
                    if self.check(TokenType.IDENTIFIER):
                        exception_type = self.current.value
                        self.advance()
                    if self.check_symbol(":"):
                        self.advance()
                        variable = self.expect(TokenType.IDENTIFIER).value
                    self.expect_symbol(")")

                self.skip_newline()

                catch_body = []

                while not self.is_end() and not self.check_keyword("FINALLY") and not self.check_keyword("END"):

                    catch_body.append(self.parse_statement())

                    self.skip_newline()

                catch_clause = CatchNode(exception_type, variable, catch_body)

            elif self.check_keyword("FINALLY"):

                self.advance()

                self.skip_newline()

                while not self.is_end() and not self.check_keyword("END"):

                    finally_body.append(self.parse_statement())

                    self.skip_newline()

            elif self.check_keyword("END"):

                self.advance()

                return TryNode(try_body, catch_clause, finally_body)

            else:

                try_body.append(self.parse_statement())

                self.skip_newline()

        raise ParserError("TRY block missing END")


    # =====================================
    # THROW
    # =====================================

    def parse_throw(self):

        self.expect_keyword("THROW")

        expression = self.parse_expression()

        return ThrowNode(expression)


    # =====================================
    # FUNCTION
    # =====================================

    def parse_function(self):

        self.expect_keyword("FUNC")

        name = self.expect(
            TokenType.IDENTIFIER
        ).value

        is_async = False
        if self.check_keyword("ASYNC"):
            self.advance()
            is_async = True

        # Parse parameters
        params = []
        if self.check_symbol("("):
            self.advance()
            while not self.check_symbol(")"):
                param_name = self.expect(TokenType.IDENTIFIER).value
                default_value = None
                is_rest = False

                if self.check_symbol("="):
                    self.advance()
                    default_value = self.parse_expression()

                params.append(ParamNode(param_name, default_value, is_rest))

                if not self.check_symbol(")"):
                    self.expect_symbol(",")

            self.expect_symbol(")")

        self.skip_newline()

        body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("END"):

                self.advance()

                return FunctionNode(
                    name,
                    params,
                    body,
                    is_async
                )

            body.append(
                self.parse_statement()
            )

            self.skip_newline()

        raise ParserError(
            "FUNC block missing END"
        )


    # =====================================
    # CLASS
    # =====================================

    def parse_class(self):

        self.expect_keyword("CLASS")

        name = self.expect(TokenType.IDENTIFIER).value

        extends = None
        if self.check_keyword("EXTENDS"):
            self.advance()
            extends = self.expect(TokenType.IDENTIFIER).value

        self.skip_newline()

        body = []

        while not self.is_end():

            self.skip_newline()

            if self.check_keyword("END"):

                self.advance()

                return ClassNode(name, extends, body)

            # Parse methods
            if self.check_keyword("FUNC"):

                body.append(self.parse_function())

            # Parse properties
            elif self.check_keyword("SET") or self.check_keyword("LET"):

                body.append(self.parse_set())

            else:

                self.advance()

            self.skip_newline()

        raise ParserError("CLASS block missing END")


    # =====================================
    # Identifier Statement (Assignment or Expression)
    # =====================================

    def parse_identifier_statement(self):

        name = self.expect(TokenType.IDENTIFIER).value
        target = IdentifierNode(name)

        # Function call statement: foo(a, b)
        if self.check_symbol("("):
            self.advance()
            arguments = []
            while not self.check_symbol(")"):
                arguments.append(self.parse_expression())
                if not self.check_symbol(")"):
                    self.expect_symbol(",")
            self.expect_symbol(")")
            return FunctionCallNode(name, arguments)

        # Preserve the old line-oriented alias syntax (e.g. `print "Hello"`
        # or `add 1 2`) without reserving those words as identifiers.
        if name.upper() in KEYWORD_ALIASES and not self.check(TokenType.NEWLINE) and not self.is_end():
            arguments = []
            while not self.is_end() and not self.check(TokenType.NEWLINE):
                arguments.append(self.parse_expression())
            return BuiltinCallNode(name, arguments)

        # Array index assignment
        if self.check_symbol("["):
            self.advance()
            index_expr = self.parse_expression()
            self.expect_symbol("]")
            if self.check_symbol("="):
                self.advance()
                value = self.parse_expression()
                return IndexSetNode(target, index_expr, value)
            return IndexNode(target, index_expr)

        # Property assignment
        if self.check_symbol("."):
            self.advance()
            if not (self.check(TokenType.IDENTIFIER) or self.check(TokenType.KEYWORD)):
                raise ParserError("Expected property name.")
            property_name = self.current.value
            self.advance()
            if self.check_symbol("="):
                self.advance()
                value = self.parse_expression()
                return PropertySetNode(target, property_name, value)
            return PropertyNode(target, property_name)

        return target


    # =====================================
    # Expression
    # =====================================

    def parse_expression(self):

        return self.parse_ternary()


    def parse_ternary(self):
        """条件演算子 (? :)"""

        expr = self.parse_logical_or()

        if self.check_symbol("?"):

            self.advance()

            true_expr = self.parse_expression()

            self.expect_symbol(":")

            false_expr = self.parse_expression()

            return TernaryOperationNode(expr, true_expr, false_expr)

        return expr


    def parse_logical_or(self):

        left = self.parse_logical_and()

        while self.check_keyword("OR"):

            self.advance()

            right = self.parse_logical_and()

            left = BinaryOperationNode(left, "OR", right)

        return left


    def parse_logical_and(self):

        left = self.parse_bitwise_or()

        while self.check_keyword("AND"):

            self.advance()

            right = self.parse_bitwise_or()

            left = BinaryOperationNode(left, "AND", right)

        return left


    def parse_bitwise_or(self):

        left = self.parse_bitwise_xor()

        while self.check_symbol("|"):

            self.advance()

            right = self.parse_bitwise_xor()

            left = BinaryOperationNode(left, "|", right)

        return left


    def parse_bitwise_xor(self):

        left = self.parse_bitwise_and()

        while self.check_symbol("^"):

            self.advance()

            right = self.parse_bitwise_and()

            left = BinaryOperationNode(left, "^", right)

        return left


    def parse_bitwise_and(self):

        left = self.parse_equality()

        while self.check_symbol("&"):

            self.advance()

            right = self.parse_equality()

            left = BinaryOperationNode(left, "&", right)

        return left


    def parse_equality(self):

        left = self.parse_relational()

        while (
            self.check_symbol("==") or
            self.check_symbol("!=") or
            self.check_symbol("===") or
            self.check_symbol("!==")
        ):

            operator = self.current.value

            self.advance()

            right = self.parse_relational()

            left = BinaryOperationNode(left, operator, right)

        return left


    def parse_relational(self):

        left = self.parse_shift()

        while (
            self.check_symbol("<") or
            self.check_symbol("<=") or
            self.check_symbol(">") or
            self.check_symbol(">=")
        ):

            operator = self.current.value

            self.advance()

            right = self.parse_shift()

            left = BinaryOperationNode(left, operator, right)

        return left


    def parse_shift(self):

        left = self.parse_additive()

        while (
            self.check_symbol("<<") or
            self.check_symbol(">>") or
            self.check_symbol(">>>")
        ):

            operator = self.current.value

            self.advance()

            right = self.parse_additive()

            left = BinaryOperationNode(left, operator, right)

        return left


    def parse_additive(self):

        left = self.parse_multiplicative()

        while (
            self.check_symbol("+") or
            self.check_symbol("-")
        ):

            operator = self.current.value

            self.advance()

            right = self.parse_multiplicative()

            left = BinaryOperationNode(left, operator, right)

        return left


    def parse_multiplicative(self):

        left = self.parse_exponential()

        while (
            self.check_symbol("*") or
            self.check_symbol("/") or
            self.check_symbol("%")
        ):

            operator = self.current.value

            self.advance()

            right = self.parse_exponential()

            left = BinaryOperationNode(left, operator, right)

        return left


    def parse_exponential(self):

        left = self.parse_unary()

        if self.check_symbol("**"):

            self.advance()

            right = self.parse_exponential()

            return BinaryOperationNode(left, "**", right)

        return left


    def parse_unary(self):

        if self.check_keyword("NOT") or self.check_symbol("!"):

            self.advance()

            value = self.parse_unary()

            return UnaryOperationNode("NOT", value)

        if self.check_symbol("-"):

            self.advance()

            value = self.parse_unary()

            return UnaryOperationNode("-", value)

        if self.check_symbol("+"):

            self.advance()

            value = self.parse_unary()

            return UnaryOperationNode("+", value)

        if self.check_symbol("~"):

            self.advance()

            value = self.parse_unary()

            return UnaryOperationNode("~", value)

        return self.parse_postfix()


    def parse_postfix(self):

        expr = self.parse_primary()

        while True:

            # Array/Object indexing
            if self.check_symbol("["):

                self.advance()

                index = self.parse_expression()

                self.expect_symbol("]")

                expr = IndexNode(expr, index)

            # Property access
            elif self.check_symbol("."):

                self.advance()

                if not (self.check(TokenType.IDENTIFIER) or self.check(TokenType.KEYWORD)):
                    raise ParserError("Expected property name.")
                property_name = self.current.value
                self.advance()

                expr = PropertyNode(expr, property_name)

            # Function call
            elif self.check_symbol("(") and isinstance(expr, IdentifierNode):

                self.advance()

                arguments = []

                while not self.check_symbol(")"):

                    arguments.append(self.parse_expression())

                    if not self.check_symbol(")"):

                        self.expect_symbol(",")

                self.expect_symbol(")")

                expr = FunctionCallNode(expr.name, arguments)

            else:

                break

        return expr


    # =====================================
    # Primary
    # =====================================

    def parse_primary(self):

        # Numbers
        if self.check(TokenType.NUMBER):

            value = self.current.value

            self.advance()

            return NumberNode(value)

        # Strings
        if self.check(TokenType.STRING):

            value = self.current.value

            self.advance()

            return StringNode(value)

        # Booleans
        if self.check_keyword("TRUE"):

            self.advance()

            return BooleanNode(True)

        if self.check_keyword("FALSE"):

            self.advance()

            return BooleanNode(False)

        # Null
        if self.check_keyword("NULL"):

            self.advance()

            return NullNode()

        # Reserved operation used as an expression (e.g. SET x = ADD(1, 2)).
        if self.current is not None and self.current.type == TokenType.KEYWORD:
            if not any(self.check_keyword(k) for k in ("LAMBDA","TRUE","FALSE","NULL","EXIT","RETURN","END","ELSE","CASE","DEFAULT","BREAK","CONTINUE","SET","LET","CONST","FUNC","CLASS","IMPORT","ASSET","WHEN","SWITCH","LOOP","WHILE","FOR","FOREACH","TRY","CATCH","FINALLY","THROW")):
                return self.parse_builtin_statement()

        # Identifier
        if self.check(TokenType.IDENTIFIER):

            name = self.current.value

            self.advance()

            return IdentifierNode(name)

        # Parenthesized expression
        if self.check_symbol("("):

            self.advance()

            expr = self.parse_expression()

            self.expect_symbol(")")

            return expr

        # Array literal
        if self.check_symbol("["):

            return self.parse_array_literal()

        # Map/Object literal
        if self.check_symbol("{"):

            return self.parse_map_literal()

        # Lambda
        if self.check_keyword("LAMBDA"):

            return self.parse_lambda()

        raise ParserError(
            f"Unexpected token in primary: {self.current}"
        )


    # =====================================
    # Array Literal
    # =====================================

    def parse_array_literal(self):

        self.expect_symbol("[")

        elements = []

        while not self.check_symbol("]"):

            elements.append(self.parse_expression())

            if not self.check_symbol("]"):

                self.expect_symbol(",")

        self.expect_symbol("]")

        return ArrayNode(elements)


    # =====================================
    # Map/Object Literal
    # =====================================

    def parse_map_literal(self):

        self.expect_symbol("{")

        self.skip_newline()

        pairs = []

        while not self.check_symbol("}"):

            self.skip_newline()

            # Key (string or identifier)
            if self.check(TokenType.STRING):

                key = StringNode(self.current.value)

                self.advance()

            elif self.check(TokenType.IDENTIFIER):

                key = StringNode(self.current.value)

                self.advance()

            else:

                raise ParserError("Expected key in map literal")

            self.expect_symbol(":")

            value = self.parse_expression()

            pairs.append((key, value))

            if not self.check_symbol("}"):

                self.expect_symbol(",")

            self.skip_newline()

        self.expect_symbol("}")

        map_node = MapNode()
        map_node.pairs = pairs
        return map_node


    # =====================================
    # Lambda
    # =====================================

    def parse_lambda(self):

        self.expect_keyword("LAMBDA")

        params = []

        if self.check_symbol("("):

            self.advance()

            while not self.check_symbol(")"):

                param_name = self.expect(TokenType.IDENTIFIER).value

                params.append(ParamNode(param_name))

                if not self.check_symbol(")"):

                    self.expect_symbol(",")

            self.expect_symbol(")")

        self.expect_symbol("=>")

        # Lambda body can be a single expression or a block
        if self.check_symbol("{"):

            self.advance()

            body = []

            while not self.check_symbol("}"):

                body.append(self.parse_statement())

            self.expect_symbol("}")

        else:

            body = [ReturnNode(self.parse_expression())]

        return LambdaNode(params, body)
