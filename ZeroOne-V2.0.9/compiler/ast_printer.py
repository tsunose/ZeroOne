"""
ZeroOne Compiler

ast_printer.py

Version 1.0.0
"""


from compiler.ast import *





class ASTPrinter:



    def __init__(self):

        self.indent = 0





    # ==========================
    # Utility
    # ==========================


    def write_indent(self):

        print(
            "    " * self.indent,
            end=""
        )




    def println(
        self,
        text
    ):

        self.write_indent()

        print(text)





    # ==========================
    # Entry
    # ==========================


    def print(
        self,
        node
    ):

        self.visit(
            node
        )





    # ==========================
    # Visitor
    # ==========================


    def visit(
        self,
        node
    ):


        if node is None:

            self.println(
                "None"
            )

            return




        if isinstance(
            node,
            ProgramNode
        ):

            self.visit_program(node)



        elif isinstance(
            node,
            NumberNode
        ):

            self.visit_number(node)



        elif isinstance(
            node,
            StringNode
        ):

            self.visit_string(node)



        elif isinstance(
            node,
            IdentifierNode
        ):

            self.visit_identifier(node)



        elif isinstance(
            node,
            BinaryOperationNode
        ):

            self.visit_binary(node)



        elif isinstance(
            node,
            UnaryOperationNode
        ):

            self.visit_unary(node)



        elif isinstance(
            node,
            SetNode
        ):

            self.visit_set(node)



        elif isinstance(
            node,
            OutNode
        ):

            self.visit_out(node)



        elif isinstance(
            node,
            ReturnNode
        ):

            self.visit_return(node)



        elif isinstance(
            node,
            ExitNode
        ):

            self.visit_exit(node)



        elif isinstance(
            node,
            ImportNode
        ):

            self.visit_import(node)



        elif isinstance(
            node,
            AssetNode
        ):

            self.visit_asset(node)



        elif isinstance(
            node,
            WhenNode
        ):

            self.visit_when(node)



        elif isinstance(
            node,
            LoopNode
        ):

            self.visit_loop(node)



        elif isinstance(
            node,
            FunctionNode
        ):

            self.visit_function(node)



        else:


            self.println(
                f"Unknown Node: {type(node).__name__}"
            )





    # ==========================
    # Program
    # ==========================


    def visit_program(
        self,
        node
    ):


        self.println(
            "Program"
        )


        self.indent += 1



        for statement in node.statements:

            self.visit(
                statement
            )



        self.indent -= 1





    # ==========================
    # Values
    # ==========================


    def visit_number(
        self,
        node
    ):

        self.println(
            f"Number({node.value})"
        )




    def visit_string(
        self,
        node
    ):

        self.println(
            f'String("{node.value}")'
        )




    def visit_identifier(
        self,
        node
    ):

        self.println(
            f"Identifier({node.name})"
        )





    # ==========================
    # Operations
    # ==========================


    def visit_binary(
        self,
        node
    ):


        self.println(
            f"Binary({node.operator})"
        )


        self.indent += 1


        self.visit(
            node.left
        )


        self.visit(
            node.right
        )


        self.indent -= 1





    def visit_unary(
        self,
        node
    ):


        self.println(
            f"Unary({node.operator})"
        )


        self.indent += 1


        self.visit(
            node.value
        )


        self.indent -= 1





    # ==========================
    # Statements
    # ==========================


    def visit_set(
        self,
        node
    ):


        self.println(
            f"Set({node.name})"
        )


        self.indent += 1


        self.visit(
            node.value
        )


        self.indent -= 1





    def visit_out(
        self,
        node
    ):


        self.println(
            "Out"
        )


        self.indent += 1


        self.visit(
            node.value
        )


        self.indent -= 1





    def visit_return(
        self,
        node
    ):


        self.println(
            "Return"
        )


        self.indent += 1


        self.visit(
            node.value
        )


        self.indent -= 1





    def visit_exit(
        self,
        node
    ):


        self.println(
            "Exit"
        )





    def visit_import(
        self,
        node
    ):


        self.println(
            f'Import("{node.filename}")'
        )





    def visit_asset(
        self,
        node
    ):


        self.println(
            f'Asset("{node.filename}")'
        )





    # ==========================
    # WHEN
    # ==========================


    def visit_when(
        self,
        node
    ):


        self.println(
            "When"
        )


        self.indent += 1



        self.println(
            "Condition"
        )


        self.indent += 1


        self.visit(
            node.condition
        )


        self.indent -= 1




        self.println(
            "Body"
        )


        self.indent += 1


        for statement in node.body:

            self.visit(
                statement
            )


        self.indent -= 1




        if node.else_body:


            self.println(
                "Else"
            )


            self.indent += 1


            for statement in node.else_body:

                self.visit(
                    statement
                )


            self.indent -= 1



        self.indent -= 1





    # ==========================
    # LOOP
    # ==========================


    def visit_loop(
        self,
        node
    ):


        self.println(
            "Loop"
        )


        self.indent += 1


        self.println(
            "Count"
        )


        self.indent += 1


        self.visit(
            node.count
        )


        self.indent -= 1



        self.println(
            "Body"
        )


        self.indent += 1


        for statement in node.body:

            self.visit(
                statement
            )


        self.indent -= 2





    # ==========================
    # Function
    # ==========================


    def visit_function(
        self,
        node
    ):


        self.println(
            f"Function({node.name})"
        )


        self.indent += 1



        if node.params:


            self.println(
                "Parameters"
            )


            self.indent += 1


            for param in node.params:

                self.println(
                    param
                )


            self.indent -= 1




        self.println(
            "Body"
        )


        self.indent += 1



        for statement in node.body:

            self.visit(
                statement
            )



        self.indent -= 2