"""
ZeroOne Compiler

generator.py

Version 3.0.0 - Extended Code Generator
"""

from compiler.ast import *
from compiler.opcode import OpCode, NATIVE_IDS
from compiler.errors import GeneratorError


class Generator:

    def __init__(self):

        self.code = []

        self.label_counter = 0

        self.function_table = {}

        self.class_table = {}

        self.loop_stack = []  # For break/continue

        self.function_depth = 0

    # ==========================
    # Utility
    # ==========================

    def reset(self):

        self.code.clear()

        self.label_counter = 0

        self.function_table.clear()

        self.class_table.clear()

        self.loop_stack.clear()

        self.function_depth = 0

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

        if node is None:
            self.emit(OpCode.PUSH, None)
            return

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
            NullNode
        ):

            self.emit(
                OpCode.PUSH,
                None
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

            operator_map = {
                "NOT": OpCode.NOT,
                "-": OpCode.NEG,
                "+": OpCode.PUSH,  # Unary plus
                "~": OpCode.BITNOT,
            }

            opcode = operator_map.get(node.operator)

            if opcode is None:
                raise GeneratorError(
                    f"Unknown unary operator: {node.operator}"
                )

            self.emit(opcode)

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

        if isinstance(
            node,
            TernaryOperationNode
        ):

            self.generate_ternary(node)
            return

        if isinstance(
            node,
            IndexNode
        ):

            self.generate_expression(node.target)
            self.generate_expression(node.index)
            self.emit(OpCode.ARRAY_GET)
            return

        if isinstance(
            node,
            PropertyNode
        ):

            self.generate_expression(node.target)
            self.emit(OpCode.GET_PROP, node.property_name)
            return

        if isinstance(
            node,
            ArrayNode
        ):

            self.emit(OpCode.ARRAY_NEW)

            for element in node.elements:
                self.generate_expression(element)
                self.emit(OpCode.ARRAY_PUSH)

            return

        if isinstance(
            node,
            MapNode
        ):

            self.emit(OpCode.MAP_NEW)

            for key, value in node.pairs:
                self.generate_expression(key)
                self.generate_expression(value)
                self.emit(OpCode.MAP_SET)

            return

        if isinstance(
            node,
            FunctionCallNode
        ):

            for arg in node.arguments:
                self.generate_expression(arg)

            self.emit(OpCode.CALL, "FUNC_" + node.name)
            return

        if isinstance(node, BuiltinCallNode):
            self.generate_builtin(node)
            return

        if isinstance(
            node,
            LambdaNode
        ):

            self.emit(OpCode.LAMBDA)
            # Body will be compiled separately
            for stmt in node.body:
                self.generate_statement(stmt)

            return

        raise GeneratorError(
            f"Unknown expression node: {type(node).__name__}"
        )

    # ==========================
    # Built-ins
    # ==========================

    def generate_builtin(self, node):
        name = node.name.upper()
        # Direct canonical aliases used by the source language.
        aliases = {
            "PRINT":"OUT", "SHOW":"OUT", "DISPLAY":"OUT", "ECHO":"OUT",
            "INPUT":"IN", "READ":"IN", "GET":"IN",
            "IF":"WHEN", "FUNCTION":"FUNC",
        }
        name = aliases.get(name, name)
        if name == "OUT":
            if node.arguments:
                self.generate_expression(node.arguments[0])
            else:
                self.emit(OpCode.PUSH, "")
            self.emit(OpCode.PRINT)
            return
        if name == "IN":
            # Native input is expression-capable.
            self.emit(OpCode.CALL_NATIVE, NATIVE_IDS.get("INPUT", 0))
            self.emit(OpCode.PUSH, 0)
            return
        native_id = NATIVE_IDS.get(name)
        if native_id is None:
            # Canonical category words that are only reservations are harmless
            # no-ops until a dedicated semantic is assigned.
            self.emit(OpCode.NOP)
            return
        for arg in node.arguments:
            self.generate_expression(arg)
        self.emit(OpCode.PUSH, len(node.arguments))
        self.emit(OpCode.CALL_NATIVE, native_id)

    # ==========================
    # Ternary Operation
    # ==========================

    def generate_ternary(self, node):

        else_label = self.new_label()
        end_label = self.new_label()

        self.generate_expression(node.condition)

        self.emit(OpCode.JMP_IF_FALSE, else_label)

        self.generate_expression(node.true_value)

        self.emit(OpCode.JMP, end_label)

        self.place_label(else_label)

        self.generate_expression(node.false_value)

        self.place_label(end_label)

    # ==========================
    # Binary Operation
    # ==========================

    def generate_binary(
        self,
        operator
    ):

        table = {
            # Arithmetic
            "+": OpCode.ADD,
            "-": OpCode.SUB,
            "*": OpCode.MUL,
            "/": OpCode.DIV,
            "%": OpCode.MOD,
            "**": OpCode.POWER,

            # Comparison
            "==": OpCode.EQ,
            "!=": OpCode.NE,
            "<": OpCode.LT,
            "<=": OpCode.LE,
            ">": OpCode.GT,
            ">=": OpCode.GE,
            "===": OpCode.EQ,  # Strict equality
            "!==": OpCode.NE,  # Strict inequality

            # Logical
            "AND": OpCode.AND,
            "OR": OpCode.OR,

            # Bitwise
            "&": OpCode.BITAND,
            "|": OpCode.BITOR,
            "^": OpCode.BITXOR,
            "<<": OpCode.LSHIFT,
            ">>": OpCode.RSHIFT,
            ">>>": OpCode.ARSHIFT,
        }

        key = operator.upper() if operator.isalpha() else operator

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

        if node is None or isinstance(node, NoOpNode):
            return

        if isinstance(node, BuiltinCallNode):
            self.generate_builtin(node)
            if node.name.upper() not in {"OUT","PRINT","SHOW","DISPLAY","ECHO"}:
                # Statements discard returned values to keep the VM stack clean.
                self.emit(OpCode.POP)
            return

        if isinstance(node, (IdentifierNode, NumberNode, StringNode, BooleanNode, NullNode, BinaryOperationNode, UnaryOperationNode, TernaryOperationNode, FunctionCallNode, ArrayNode, MapNode, IndexNode, PropertyNode)):
            self.generate_expression(node)
            self.emit(OpCode.POP)
            return

        if isinstance(
            node,
            SetNode
        ):

            self.generate_expression(
                node.value
            )

            self.emit(
                OpCode.STORE_LOCAL if self.function_depth else OpCode.STORE,
                node.name
            )

            return

        if isinstance(
            node,
            OutNode
        ):

            if node.value is not None:
                self.generate_expression(
                    node.value
                )
            else:
                self.emit(OpCode.PUSH, "")

            self.emit(
                OpCode.PRINT
            )

            return

        if isinstance(
            node,
            ReturnNode
        ):

            if node.value is not None:
                self.generate_expression(
                    node.value
                )
            else:
                self.emit(OpCode.PUSH, None)

            self.emit(
                OpCode.RETURN
            )

            return

        if isinstance(
            node,
            ExitNode
        ):

            self.emit(
                OpCode.EXIT,
                node.code
            )

            return

        if isinstance(
            node,
            ImportNode
        ):

            # Reserved for future implementation
            return

        if isinstance(
            node,
            AssetNode
        ):

            # Reserved for future implementation
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
            SwitchNode
        ):

            self.generate_switch(node)
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
            WhileNode
        ):

            self.generate_while(node)
            return

        if isinstance(
            node,
            ForNode
        ):

            self.generate_for(node)
            return

        if isinstance(
            node,
            ForEachNode
        ):

            self.generate_foreach(node)
            return

        if isinstance(
            node,
            BreakNode
        ):

            if self.loop_stack:
                self.emit(OpCode.JMP, self.loop_stack[-1]["end"])
            return

        if isinstance(
            node,
            ContinueNode
        ):

            if self.loop_stack:
                self.emit(OpCode.JMP, self.loop_stack[-1]["start"])
            return

        if isinstance(
            node,
            TryNode
        ):

            self.generate_try(node)
            return

        if isinstance(
            node,
            ThrowNode
        ):

            self.generate_expression(node.expression)
            self.emit(OpCode.THROW)
            return

        if isinstance(
            node,
            FunctionNode
        ):

            self.generate_function(
                node
            )

            return

        if isinstance(
            node,
            ClassNode
        ):

            self.generate_class(node)
            return

        if isinstance(
            node,
            IndexSetNode
        ):

            self.generate_expression(node.target)
            self.generate_expression(node.index)
            self.generate_expression(node.value)
            self.emit(OpCode.ARRAY_SET)
            return

        if isinstance(
            node,
            PropertySetNode
        ):

            self.generate_expression(node.target)
            self.generate_expression(node.value)
            self.emit(OpCode.SET_PROP, node.property_name)
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
    # SWITCH
    # ==========================

    def generate_switch(self, node):

        end_label = self.new_label()

        self.generate_expression(node.expression)

        case_labels = []

        for case in node.cases:
            case_label = self.new_label()
            case_labels.append(case_label)

            self.emit(OpCode.DUP)
            self.generate_expression(case.value)
            self.emit(OpCode.EQ)
            self.emit(OpCode.JMP_IF_TRUE, case_label)

        default_label = self.new_label() if node.default_body else end_label

        self.emit(OpCode.JMP, default_label)

        for i, case in enumerate(node.cases):
            self.place_label(case_labels[i])
            for stmt in case.body:
                self.generate_statement(stmt)
            self.emit(OpCode.JMP, end_label)

        if node.default_body:
            self.place_label(default_label)
            for stmt in node.default_body:
                self.generate_statement(stmt)

        self.place_label(end_label)
        self.emit(OpCode.POP)  # Remove comparison value from stack

    # ==========================
    # LOOP
    # ==========================

    def generate_loop(
        self,
        node
    ):

        start_label = self.new_label()
        end_label = self.new_label()

        self.loop_stack.append({
            "start": start_label,
            "end": end_label
        })

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

        self.loop_stack.pop()

    # ==========================
    # WHILE
    # ==========================

    def generate_while(self, node):

        start_label = self.new_label()
        end_label = self.new_label()

        self.loop_stack.append({
            "start": start_label,
            "end": end_label
        })

        self.place_label(start_label)

        self.generate_expression(node.condition)

        self.emit(OpCode.JMP_IF_FALSE, end_label)

        for stmt in node.body:
            self.generate_statement(stmt)

        self.emit(OpCode.JMP, start_label)

        self.place_label(end_label)

        self.loop_stack.pop()

    # ==========================
    # FOR
    # ==========================

    def generate_for(self, node):

        if node.init:
            self.generate_statement(node.init)

        start_label = self.new_label()
        end_label = self.new_label()

        self.loop_stack.append({
            "start": start_label,
            "end": end_label
        })

        self.place_label(start_label)

        if node.condition:
            self.generate_expression(node.condition)
        else:
            self.emit(OpCode.PUSH, True)

        self.emit(OpCode.JMP_IF_FALSE, end_label)

        for stmt in node.body:
            self.generate_statement(stmt)

        if node.update:
            self.generate_statement(node.update)

        self.emit(OpCode.JMP, start_label)

        self.place_label(end_label)

        self.loop_stack.pop()

    # ==========================
    # FOREACH
    # ==========================

    def generate_foreach(self, node):

        start_label = self.new_label()
        end_label = self.new_label()

        self.loop_stack.append({
            "start": start_label,
            "end": end_label
        })

        # Evaluate iterable and iterate
        self.generate_expression(node.iterable)
        self.emit(OpCode.ITERATOR)

        self.place_label(start_label)

        self.emit(OpCode.NEXT)
        self.emit(OpCode.JMP_IF_NULL, end_label)

        self.emit(OpCode.STORE, node.variable)

        for stmt in node.body:
            self.generate_statement(stmt)

        self.emit(OpCode.JMP, start_label)

        self.place_label(end_label)

        self.loop_stack.pop()

    # ==========================
    # TRY-CATCH-FINALLY
    # ==========================

    def generate_try(self, node):

        try_label = self.new_label()
        catch_label = self.new_label() if node.catch_clause else None
        finally_label = self.new_label() if node.finally_body else None
        end_label = self.new_label()

        self.place_label(try_label)

        self.emit(OpCode.TRY, catch_label if catch_label else end_label)

        for stmt in node.body:
            self.generate_statement(stmt)

        if catch_label:
            self.place_label(catch_label)
            self.emit(OpCode.CATCH, node.catch_clause.exception_type)

            for stmt in node.catch_clause.body:
                self.generate_statement(stmt)

        if finally_label:
            self.place_label(finally_label)

            for stmt in node.finally_body:
                self.generate_statement(stmt)

        self.place_label(end_label)

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

        self.function_table[node.name] = label

        skip_label = self.new_label()
        self.emit(OpCode.JMP, skip_label)
        self.place_label(label)

        self.function_depth += 1
        # CALL leaves arguments on the stack. Bind them right-to-left so
        # f(a,b) receives the original argument order.
        for param in reversed(node.params):
            if getattr(param, "is_rest", False):
                self.emit(OpCode.STORE_LOCAL, param.name)
            else:
                self.emit(OpCode.STORE_LOCAL, param.name)
        for statement in node.body:
            self.generate_statement(statement)
        self.emit(OpCode.PUSH, None)
        self.emit(OpCode.RETURN)
        self.function_depth -= 1

        self.place_label(skip_label)

    # ==========================
    # CLASS
    # ==========================

    def generate_class(self, node):

        class_label = "CLASS_" + node.name

        if node.name in self.class_table:
            raise GeneratorError(
                f"Class '{node.name}' already exists."
            )

        self.class_table[node.name] = {
            "extends": node.extends,
            "methods": {}
        }

        self.place_label(class_label)

        for item in node.body:
            if isinstance(item, FunctionNode):
                self.generate_function(item)
            elif isinstance(item, SetNode):
                # Class property (static)
                self.generate_statement(item)

        self.emit(OpCode.RETURN)
