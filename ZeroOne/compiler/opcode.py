"""
ZeroOne Compiler

opcode.py

Version 1.0.0
"""



class OpCode:



    # ==========================
    # Stack
    # ==========================


    PUSH = 1

    POP = 2





    # ==========================
    # Memory
    # ==========================


    STORE = 10

    LOAD = 11





    # ==========================
    # Arithmetic
    # ==========================


    ADD = 20

    SUB = 21

    MUL = 22

    DIV = 23

    MOD = 24





    # ==========================
    # Compare
    # ==========================


    EQ = 30

    NE = 31

    LT = 32

    LE = 33

    GT = 34

    GE = 35





    # ==========================
    # Logic
    # ==========================


    AND = 40

    OR = 41

    NOT = 42





    # ==========================
    # Control Flow
    # ==========================


    JMP = 50

    JMP_IF_FALSE = 51

    JMP_IF_TRUE = 52


    LABEL = 53





    # ==========================
    # Function
    # ==========================


    CALL = 60

    RETURN = 61





    # ==========================
    # System
    # ==========================


    PRINT = 70


    # ==========================
    # Array
    # ==========================


    ARRAY_NEW = 80

    ARRAY_GET = 81

    ARRAY_SET = 82

    ARRAY_PUSH = 83

    ARRAY_LEN = 84


    EXIT = 99




    # ==========================
    # Debug
    # ==========================


    _NAMES = {


        1: "PUSH",

        2: "POP",



        10: "STORE",

        11: "LOAD",



        20: "ADD",

        21: "SUB",

        22: "MUL",

        23: "DIV",

        24: "MOD",



        30: "EQ",

        31: "NE",

        32: "LT",

        33: "LE",

        34: "GT",

        35: "GE",



        40: "AND",

        41: "OR",

        42: "NOT",



        50: "JMP",

        51: "JMP_IF_FALSE",

        52: "JMP_IF_TRUE",

        53: "LABEL",



        60: "CALL",

        61: "RETURN",



        70: "PRINT",


        80: "ARRAY_NEW",

        81: "ARRAY_GET",

        82: "ARRAY_SET",

        83: "ARRAY_PUSH",

        84: "ARRAY_LEN",


        99: "EXIT"

    }




    @staticmethod
    def name(code):

        return OpCode._NAMES.get(
            code,
            "UNKNOWN"
        )