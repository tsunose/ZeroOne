"""
ZeroOne Compiler

errors.py

Version 1.0.0
"""



# ==========================
# Base Error
# ==========================


class ZeroOneError(Exception):
    """
    ZeroOne全体の基本エラー
    """

    pass





# ==========================
# Lexer
# ==========================


class LexerError(ZeroOneError):
    """
    字句解析エラー
    """

    pass





# ==========================
# Parser
# ==========================


class ParserError(ZeroOneError):
    """
    構文解析エラー
    """

    pass





# ==========================
# AST / Generator
# ==========================


class GeneratorError(ZeroOneError):
    """
    ASTから命令生成時のエラー
    """

    pass





# ==========================
# Assembler
# ==========================


class AssemblerError(ZeroOneError):
    """
    アセンブラ処理エラー
    """

    pass


class CompilerError(ZeroOneError):
    """
    コンパイル処理全般のエラー
    """

    pass





# ==========================
# ByteCode
# ==========================


class ByteCodeError(ZeroOneError):
    """
    ByteCode読み書きエラー
    """

    pass





# ==========================
# Virtual Machine
# ==========================


class VMError(ZeroOneError):
    """
    VM実行エラー
    """

    pass





# ==========================
# Runtime
# ==========================


class ZeroOneRuntimeError(ZeroOneError):
    """
    実行時エラー
    """

    pass