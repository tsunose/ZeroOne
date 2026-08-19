"""
ZeroOne Compiler

generator.py

Version 2.0.0
"""

from compiler.ast import *
from compiler.opcode import OpCode
from compiler.errors import GeneratorError


class Generator:

    def __init__(self):

        self.code = []

        self.label_counter = 0

        self.function_table = {}

    # ==========================
    # Utility
    # ==========================

    def reset(self):

        self.code.clear()

        self.label_counter = 0

        self.function_table.clear()

    def emit(
        self,
        opcode,
        operand=None
    ):

        if operand is None:

            self.code.append(
                (opcode,)
            )

        else:

            self.code.append(
                (
                    opcode,
                    operand
                )
            )

    # ==========================
    # Label
    # ==========================

    def new_label(self):

        label = (
            "L"
            + str(self.label_counter)
        )

        self.label_counter += 1

        return label

    def place_label(
        self,
        label
    ):

        self.emit(
            OpCode.LABEL,
            label
        )

    # ==========================
    # Entry
    # ==========================

    def generate(
        self,
        program
    ):

        self.reset()

        if not isinstance(
            program,
            ProgramNode
        ):

            raise GeneratorError(
                "Root node must be ProgramNode."
            )

        self.generate_program(
            program
        )

        return self.code

    # ==========================
    # Program
    # ==========================

    def generate_program(
        self,
        node
    ):

        for statement in node.statements:

            self.generate_statement(
                statement
            )

    # ==========================
    # Expression
    # ==========================

    def generate_expression(
        self,
        node
    ):

        if isinstance(
            node,
            NumberNode
        ):

            self.emit(
                OpCode.PUSH,
                node.value
            )

            return

        if isinstance(
            node,
            StringNode
        ):

            self.emit(
                OpCode.PUSH,
                node.value
            )

            return

        if isinstance(
            node,
            BooleanNode
        ):

            self.emit(
                OpCode.PUSH,
                node.value
            )

            return

        if isinstance(
            node,
            IdentifierNode
        ):

            self.emit(
                OpCode.LOAD,
                node.name
            )

            return

        if isinstance(
            node,
            UnaryOperationNode
        ):

            self.generate_expression(
                node.value
            )

            if node.operator.upper() == "NOT":

                self.emit(
                    OpCode.NOT
                )

            else:

                raise GeneratorError(
                    f"Unknown unary operator: {node.operator}"
                )

            return

        if isinstance(
            node,
            BinaryOperationNode
        ):

            self.generate_expression(
                node.left
            )

            self.generate_expression(
                node.right
            )

            self.generate_binary(
                node.operator
            )

            return

        raise GeneratorError(
            f"Unknown expression node: {type(node).__name__}"
        )

    # ==========================
    # Binary Operation
    # ==========================

    def generate_binary(
        self,
        operator
    ):

        table = {

            "+": OpCode.ADD,
            "-": OpCode.SUB,
            "*": OpCode.MUL,
            "/": OpCode.DIV,
            "%": OpCode.MOD,

            "==": OpCode.EQ,
            "!=": OpCode.NE,
            "<": OpCode.LT,
            "<=": OpCode.LE,
            ">": OpCode.GT,
            ">=": OpCode.GE,

            "AND": OpCode.AND,
            "OR": OpCode.OR

        }

        key = operator.upper()

        if key not in table:

            raise GeneratorError(
                f"Unknown operator: {operator}"
            )

        self.emit(
            table[key]
        )

    # ==========================
    # Statement
    # ==========================

    def generate_statement(
        self,
        node
    ):

        if isinstance(node, NoOpNode):
            return

        if isinstance(
            node,
            SetNode
        ):

            self.generate_expression(
                node.value
            )

            self.emit(
                OpCode.STORE,
                node.name
            )

            return

        if isinstance(
            node,
            OutNode
        ):

            self.generate_expression(
                node.value
            )

            self.emit(
                OpCode.PRINT
            )

            return

        if isinstance(
            node,
            ReturnNode
        ):

            self.generate_expression(
                node.value
            )

            self.emit(
                OpCode.RETURN
            )

            return

        if isinstance(
            node,
            ExitNode
        ):

            self.emit(
                OpCode.EXIT
            )

            return

        if isinstance(
            node,
            ImportNode
        ):

            # Version 2.0.0では予約
            return

        if isinstance(
            node,
            AssetNode
        ):

            # Version 2.0.0では予約
            return

        if isinstance(
            node,
            WhenNode
        ):

            self.generate_when(
                node
            )

            return

        if isinstance(
            node,
            LoopNode
        ):

            self.generate_loop(
                node
            )

            return

        if isinstance(
            node,
            FunctionNode
        ):

            self.generate_function(
                node
            )

            return

        raise GeneratorError(
            f"Unknown statement: {type(node).__name__}"
        )

    # ==========================
    # WHEN
    # ==========================

    def generate_when(
        self,
        node
    ):

        else_label = self.new_label()
        end_label = self.new_label()

        self.generate_expression(
            node.condition
        )

        self.emit(
            OpCode.JMP_IF_FALSE,
            else_label
        )

        for statement in node.body:

            self.generate_statement(
                statement
            )

        self.emit(
            OpCode.JMP,
            end_label
        )

        self.place_label(
            else_label
        )

        for statement in node.else_body:

            self.generate_statement(
                statement
            )

        self.place_label(
            end_label
        )

    # ==========================
    # LOOP
    # ==========================

    def generate_loop(
        self,
        node
    ):

        start_label = self.new_label()
        end_label = self.new_label()

        self.place_label(
            start_label
        )

        self.generate_expression(
            node.count
        )

        self.emit(
            OpCode.JMP_IF_FALSE,
            end_label
        )

        for statement in node.body:

            self.generate_statement(
                statement
            )

        self.emit(
            OpCode.JMP,
            start_label
        )

        self.place_label(
            end_label
        )

    # ==========================
    # FUNCTION
    # ==========================

    def generate_function(
        self,
        node
    ):

        label = "FUNC_" + node.name

        if node.name in self.function_table:

            raise GeneratorError(
                f"Function '{node.name}' already exists."
            )

        self.function_table[
            node.name
        ] = label

        self.place_label(
            label
        )

        for statement in node.body:

            self.generate_statement(
                statement
            )

        self.emit(
            OpCode.RETURN
        )