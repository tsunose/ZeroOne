"""
ZeroOne Compiler

ast.py

Version 1.0.0
"""



# ==========================
# Base
# ==========================


class ASTNode:
    """
    すべてのASTノードの基底クラス
    """

    def node_name(self):

        return self.__class__.__name__





# ==========================
# Values
# ==========================


class NumberNode(ASTNode):

    def __init__(
        self,
        value
    ):

        self.value = value





class StringNode(ASTNode):

    def __init__(
        self,
        value
    ):

        self.value = value




class BooleanNode(ASTNode):

    def __init__(
        self,
        value
    ):

        self.value = bool(value)




class NoOpNode(ASTNode):
    pass




class IdentifierNode(ASTNode):

    def __init__(
        self,
        name
    ):

        self.name = name





# ==========================
# Operations
# ==========================


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





# ==========================
# Statements
# ==========================


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

    def __init__(self):

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





# ==========================
# Control Flow
# ==========================


class WhenNode(ASTNode):

    def __init__(
        self,
        condition,
        body,
        else_body=None
    ):

        self.condition = condition

        self.body = body

        self.else_body = (
            else_body
            if else_body is not None
            else []
        )





class LoopNode(ASTNode):

    def __init__(
        self,
        count,
        body
    ):

        self.count = count

        self.body = body





# ==========================
# Function
# ==========================


class FunctionNode(ASTNode):

    def __init__(
        self,
        name,
        params,
        body
    ):

        self.name = name

        self.params = (
            params
            if params is not None
            else []
        )

        self.body = body





# ==========================
# Program
# ==========================


class ProgramNode(ASTNode):

    def __init__(
        self,
        statements=None
    ):

        self.statements = (
            statements
            if statements is not None
            else []
        )




    def add(
        self,
        node
    ):

        self.statements.append(
            node
        )




# ==========================
# Array
# ==========================


class ArrayNode(ASTNode):
    """
    配列リテラル [a, b, c]
    """

    def __init__(
        self,
        elements=None
    ):

        self.elements = (
            elements
            if elements is not None
            else []
        )




class IndexNode(ASTNode):
    """
    添字アクセス（読み取り） arr[index]
    """

    def __init__(
        self,
        target,
        index
    ):

        self.target = target

        self.index = index




class IndexSetNode(ASTNode):
    """
    添字への代入 arr[index] = value
    """

    def __init__(
        self,
        target,
        index,
        value
    ):

        self.target = target

        self.index = index

        self.value = value