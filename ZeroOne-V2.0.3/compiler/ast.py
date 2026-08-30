"""
ZeroOne Compiler

ast.py

Version 3.0.0 - Extended AST Nodes
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
# Literals
# ==========================

class NumberNode(ASTNode):

    def __init__(self, value):
        self.value = value


class StringNode(ASTNode):

    def __init__(self, value):
        self.value = value


class BooleanNode(ASTNode):

    def __init__(self, value):
        self.value = bool(value)


class NullNode(ASTNode):
    pass


class IdentifierNode(ASTNode):

    def __init__(self, name):
        self.name = name


class NoOpNode(ASTNode):
    pass


# ==========================
# Operations
# ==========================

class BinaryOperationNode(ASTNode):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOperationNode(ASTNode):

    def __init__(self, operator, value):
        self.operator = operator
        self.value = value


class TernaryOperationNode(ASTNode):
    """条件演算子: condition ? true_value : false_value"""

    def __init__(self, condition, true_value, false_value):
        self.condition = condition
        self.true_value = true_value
        self.false_value = false_value


# ==========================
# Statements
# ==========================

class SetNode(ASTNode):

    def __init__(self, name, value, is_const=False):
        self.name = name
        self.value = value
        self.is_const = is_const


class OutNode(ASTNode):

    def __init__(self, value):
        self.value = value


class ReturnNode(ASTNode):

    def __init__(self, value=None):
        self.value = value


class ExitNode(ASTNode):

    def __init__(self, code=0):
        self.code = code


class ImportNode(ASTNode):

    def __init__(self, filename):
        self.filename = filename


class AssetNode(ASTNode):

    def __init__(self, filename):
        self.filename = filename


class BuiltinCallNode(ASTNode):
    """Built-in language operation call."""
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments if arguments is not None else []


# ==========================
# Control Flow
# ==========================

class WhenNode(ASTNode):
    """If-Else条件分岐"""

    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body if else_body is not None else []


class SwitchNode(ASTNode):
    """Switch-Case分岐"""

    def __init__(self, expression, cases, default_body=None):
        self.expression = expression
        self.cases = cases  # List of CaseNode
        self.default_body = default_body if default_body is not None else []


class CaseNode(ASTNode):
    """Switch内のCase"""

    def __init__(self, value, body):
        self.value = value
        self.body = body


class LoopNode(ASTNode):
    """単純なループ"""

    def __init__(self, count, body):
        self.count = count
        self.body = body


class WhileNode(ASTNode):
    """While ループ"""

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForNode(ASTNode):
    """For ループ"""

    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body


class ForEachNode(ASTNode):
    """For-Each ループ"""

    def __init__(self, variable, iterable, body):
        self.variable = variable
        self.iterable = iterable
        self.body = body


class DoWhileNode(ASTNode):
    """Do-While ループ"""

    def __init__(self, body, condition):
        self.body = body
        self.condition = condition


class BreakNode(ASTNode):
    """Loop破出"""
    pass


class ContinueNode(ASTNode):
    """Loop継続"""
    pass


# ==========================
# Exception Handling
# ==========================

class TryNode(ASTNode):
    """Try-Catch-Finally"""

    def __init__(self, body, catch_clause=None, finally_body=None):
        self.body = body
        self.catch_clause = catch_clause
        self.finally_body = finally_body if finally_body is not None else []


class CatchNode(ASTNode):
    """Catch句"""

    def __init__(self, exception_type, variable, body):
        self.exception_type = exception_type
        self.variable = variable
        self.body = body


class ThrowNode(ASTNode):
    """例外投出"""

    def __init__(self, expression):
        self.expression = expression


# ==========================
# Function
# ==========================

class FunctionNode(ASTNode):

    def __init__(self, name, params, body, is_async=False):
        self.name = name
        self.params = params if params is not None else []
        self.body = body
        self.is_async = is_async


class FunctionCallNode(ASTNode):

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class LambdaNode(ASTNode):
    """ラムダ/無名関数"""

    def __init__(self, params, body):
        self.params = params if params is not None else []
        self.body = body


class YieldNode(ASTNode):
    """Generator yield"""

    def __init__(self, value=None):
        self.value = value


class AwaitNode(ASTNode):
    """Async-await"""

    def __init__(self, expression):
        self.expression = expression


# ==========================
# Class/Object
# ==========================

class ClassNode(ASTNode):
    """クラス定義"""

    def __init__(self, name, extends=None, body=None):
        self.name = name
        self.extends = extends
        self.body = body if body is not None else []


class MethodNode(ASTNode):
    """メソッド定義"""

    def __init__(self, name, params, body, is_static=False, is_constructor=False):
        self.name = name
        self.params = params if params is not None else []
        self.body = body
        self.is_static = is_static
        self.is_constructor = is_constructor


class PropertyNode(ASTNode):
    """オブジェクトプロパティ"""

    def __init__(self, target, property_name):
        self.target = target
        self.property_name = property_name


class PropertySetNode(ASTNode):
    """プロパティ設定"""

    def __init__(self, target, property_name, value):
        self.target = target
        self.property_name = property_name
        self.value = value


class NewNode(ASTNode):
    """オブジェクト生成"""

    def __init__(self, class_name, arguments):
        self.class_name = class_name
        self.arguments = arguments


class ThisNode(ASTNode):
    """this参照"""
    pass


class SuperNode(ASTNode):
    """super参照"""
    pass


# ==========================
# Array
# ==========================

class ArrayNode(ASTNode):
    """配列リテラル [a, b, c]"""

    def __init__(self, elements=None):
        self.elements = elements if elements is not None else []


class IndexNode(ASTNode):
    """添字アクセス（読み取り） arr[index]"""

    def __init__(self, target, index):
        self.target = target
        self.index = index


class IndexSetNode(ASTNode):
    """添字への代入 arr[index] = value"""

    def __init__(self, target, index, value):
        self.target = target
        self.index = index
        self.value = value


class SliceNode(ASTNode):
    """配列スライス arr[start:end]"""

    def __init__(self, target, start=None, end=None):
        self.target = target
        self.start = start
        self.end = end


class ArrayMethodNode(ASTNode):
    """配列メソッド呼び出し (map, filter, reduce等)"""

    def __init__(self, array, method, arguments):
        self.array = array
        self.method = method
        self.arguments = arguments


# ==========================
# Map/Dictionary/Object
# ==========================

class MapNode(ASTNode):
    """マップリテラル {key: value, ...}"""

    def __init__(self, pairs=None):
        self.pairs = pairs if pairs is not None else []  # List of (key, value) tuples


class MapEntryNode(ASTNode):
    """マップエントリ"""

    def __init__(self, key, value):
        self.key = key
        self.value = value


# ==========================
# String Operations
# ==========================

class StringInterpolationNode(ASTNode):
    """文字列補間"""

    def __init__(self, parts):
        self.parts = parts  # Mix of StringNode and expression nodes


class StringMethodNode(ASTNode):
    """文字列メソッド (upper, lower, split等)"""

    def __init__(self, string, method, arguments):
        self.string = string
        self.method = method
        self.arguments = arguments


# ==========================
# Type Operations
# ==========================

class TypeCheckNode(ASTNode):
    """型チェック: typeof x, x instanceof Class"""

    def __init__(self, expression, type_name):
        self.expression = expression
        self.type_name = type_name


class CastNode(ASTNode):
    """型キャスト: (int)x, x as float"""

    def __init__(self, expression, target_type):
        self.expression = expression
        self.target_type = target_type


# ==========================
# Advanced Features
# ==========================

class SpreadNode(ASTNode):
    """スプレッド演算子: ...array"""

    def __init__(self, expression):
        self.expression = expression


class RestNode(ASTNode):
    """Rest パラメータ: ...args"""

    def __init__(self, name):
        self.name = name


class DestructureNode(ASTNode):
    """デストラクチャ代入: [a, b] = arr, {x, y} = obj"""

    def __init__(self, pattern, expression):
        self.pattern = pattern
        self.expression = expression


class ConditionalNode(ASTNode):
    """条件式: if condition then value1 else value2"""

    def __init__(self, condition, true_expr, false_expr):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr


class MatchNode(ASTNode):
    """パターンマッチング"""

    def __init__(self, expression, patterns):
        self.expression = expression
        self.patterns = patterns  # List of (pattern, body) tuples


class PatternNode(ASTNode):
    """マッチパターン"""

    def __init__(self, pattern):
        self.pattern = pattern


# ==========================
# Regular Expression
# ==========================

class RegexNode(ASTNode):
    """正規表現リテラル"""

    def __init__(self, pattern, flags=""):
        self.pattern = pattern
        self.flags = flags


class RegexMethodNode(ASTNode):
    """正規表現メソッド (match, replace, split等)"""

    def __init__(self, regex, method, arguments):
        self.regex = regex
        self.method = method
        self.arguments = arguments


# ==========================
# Miscellaneous
# ==========================

class BlockNode(ASTNode):
    """コードブロック"""

    def __init__(self, statements=None):
        self.statements = statements if statements is not None else []


class ProgramNode(ASTNode):
    """プログラム全体"""

    def __init__(self, statements=None):
        self.statements = statements if statements is not None else []

    def add(self, node):
        self.statements.append(node)


class CommentNode(ASTNode):
    """コメント"""

    def __init__(self, text):
        self.text = text


class EnumNode(ASTNode):
    """Enum定義"""

    def __init__(self, name, members):
        self.name = name
        self.members = members  # List of (name, value) tuples


class StructNode(ASTNode):
    """Struct定義"""

    def __init__(self, name, fields):
        self.name = name
        self.fields = fields  # List of (name, type) tuples


class NamespaceNode(ASTNode):
    """名前空間"""

    def __init__(self, name, body):
        self.name = name
        self.body = body


class AssertNode(ASTNode):
    """Assertion"""

    def __init__(self, condition, message=None):
        self.condition = condition
        self.message = message


class DebugNode(ASTNode):
    """デバッグ出力"""

    def __init__(self, value):
        self.value = value


class AttributeNode(ASTNode):
    """属性/デコレータ"""

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class InlineAsmNode(ASTNode):
    """インラインアセンブリ"""

    def __init__(self, code):
        self.code = code


class ParamNode(ASTNode):
    """関数パラメータ"""

    def __init__(self, name, default_value=None, is_rest=False):
        self.name = name
        self.default_value = default_value
        self.is_rest = is_rest
