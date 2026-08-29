"""
ZeroOne Compiler

opcode.py

Version 3.0.0 - Extended with 100+ opcodes
"""


class OpCode:

    # ==========================
    # Stack Operations (1-9)
    # ==========================

    PUSH = 1
    POP = 2
    DUP = 3
    SWAP = 4
    ROT = 5  # Rotate top 3 stack values
    OVER = 6  # Copy second value to top
    DEPTH = 7  # Get stack depth
    CLEAR_STACK = 8  # Clear entire stack


    # ==========================
    # Memory Operations (10-29)
    # ==========================

    STORE = 10
    LOAD = 11
    STORE_GLOBAL = 12
    LOAD_GLOBAL = 13
    STORE_LOCAL = 14
    LOAD_LOCAL = 15
    ALLOC = 16  # Allocate memory
    FREE = 17  # Free memory
    COPY_MEMORY = 18
    ZERO_MEMORY = 19
    MOVE_MEMORY = 20
    HEAP_PUSH = 21
    HEAP_POP = 22
    HEAP_PEEK = 23
    SET_REF = 24  # Set reference
    GET_REF = 25  # Get reference


    # ==========================
    # Arithmetic Operations (30-59)
    # ==========================

    ADD = 30
    SUB = 31
    MUL = 32
    DIV = 33
    MOD = 34
    POWER = 35
    NEG = 36
    ABS = 37
    SQRT = 38
    EXP = 39
    LN = 40
    LOG = 41
    LOG10 = 42
    SIN = 43
    COS = 44
    TAN = 45
    ASIN = 46
    ACOS = 47
    ATAN = 48
    FLOOR = 49
    CEIL = 50
    ROUND = 51
    TRUNC = 52
    MAX = 53
    MIN = 54
    CLAMP = 55
    SIGN = 56
    FAC = 57  # Factorial


    # ==========================
    # Comparison (60-79)
    # ==========================

    EQ = 60
    NE = 61
    LT = 62
    LE = 63
    GT = 64
    GE = 65
    CMP = 66  # Three-way comparison
    ISNULL = 67
    ISNOTNULL = 68
    ISNAN = 69
    ISINF = 70


    # ==========================
    # Logical Operations (80-99)
    # ==========================

    AND = 80
    OR = 81
    NOT = 82
    XOR = 83
    NAND = 84
    NOR = 85
    XNOR = 86


    # ==========================
    # Bitwise Operations (100-119)
    # ==========================

    BITAND = 100
    BITOR = 101
    BITXOR = 102
    BITNOT = 103
    LSHIFT = 104
    RSHIFT = 105
    ARSHIFT = 106  # Arithmetic right shift
    ROTL = 107  # Rotate left
    ROTR = 108  # Rotate right
    POPCOUNT = 109  # Count set bits
    CLZA = 110  # Count leading zeros
    CTZB = 111  # Count trailing zeros


    # ==========================
    # String Operations (120-149)
    # ==========================

    STR_PUSH = 120
    STR_POP = 121
    STR_CONCAT = 122
    STR_LEN = 123
    STR_SUBSTR = 124
    STR_FIND = 125
    STR_REPLACE = 126
    STR_UPPER = 127
    STR_LOWER = 128
    STR_TRIM = 129
    STR_SPLIT = 130
    STR_JOIN = 131
    STR_COMPARE = 132
    STR_STARTSWITH = 133
    STR_ENDSWITH = 134
    STR_CONTAINS = 135
    STR_INDEX = 136
    STR_REVERSE = 137
    STR_REPEAT = 138
    STR_FORMAT = 139
    STR_ENCODE = 140
    STR_DECODE = 141
    CHAR_CODE = 142
    CODE_CHAR = 143


    # ==========================
    # Array Operations (150-189)
    # ==========================

    ARRAY_NEW = 150
    ARRAY_GET = 151
    ARRAY_SET = 152
    ARRAY_PUSH = 153
    ARRAY_POP = 154
    ARRAY_LEN = 155
    ARRAY_SHIFT = 156
    ARRAY_UNSHIFT = 157
    ARRAY_SLICE = 158
    ARRAY_SPLICE = 159
    ARRAY_CONCAT = 160
    ARRAY_REVERSE = 161
    ARRAY_SORT = 162
    ARRAY_FIND = 163
    ARRAY_FINDINDEX = 164
    ARRAY_INCLUDES = 165
    ARRAY_INDEXOF = 166
    ARRAY_LASTINDEXOF = 167
    ARRAY_MAP = 168
    ARRAY_FILTER = 169
    ARRAY_REDUCE = 170
    ARRAY_FOREACH = 171
    ARRAY_FILL = 172
    ARRAY_COPY = 173
    ARRAY_CLEAR = 174
    ARRAY_REMOVE = 175
    ARRAY_INSERT = 176
    ARRAY_SUM = 177
    ARRAY_AVG = 178
    ARRAY_MAX = 179
    ARRAY_MIN = 180
    ARRAY_ALL = 181  # Check if all elements match condition
    ARRAY_ANY = 182  # Check if any element matches condition
    ARRAY_UNIQUE = 183  # Remove duplicates
    ARRAY_FLAT = 184  # Flatten nested arrays
    ARRAY_CHUNK = 185  # Split into chunks
    ARRAY_ZIP = 186  # Zip multiple arrays


    # ==========================
    # Map/Dictionary Operations (190-209)
    # ==========================

    MAP_NEW = 190
    MAP_SET = 191
    MAP_GET = 192
    MAP_DEL = 193
    MAP_HAS = 194
    MAP_KEYS = 195
    MAP_VALUES = 196
    MAP_SIZE = 197
    MAP_CLEAR = 198
    MAP_COPY = 199
    MAP_MERGE = 200


    # ==========================
    # Type Operations (210-229)
    # ==========================

    TYPE_OF = 210
    TYPE_CHECK = 211
    CAST_INT = 212
    CAST_FLOAT = 213
    CAST_STR = 214
    CAST_BOOL = 215
    CAST_ARRAY = 216
    CAST_MAP = 217
    IS_INT = 218
    IS_FLOAT = 219
    IS_STR = 220
    IS_BOOL = 221
    IS_ARRAY = 222
    IS_MAP = 223
    IS_CALLABLE = 224
    IS_NUMERIC = 225


    # ==========================
    # Control Flow (230-259)
    # ==========================

    JMP = 230
    JMP_IF_TRUE = 231
    JMP_IF_FALSE = 232
    JMP_IF_NULL = 233
    JMP_IF_NOTNULL = 234
    LABEL = 235
    COND_JMP = 236  # Conditional jump
    LOOP = 237
    LOOP_WHILE = 238
    LOOP_UNTIL = 239
    BREAK = 240
    CONTINUE = 241
    CASE = 242
    SWITCH = 243
    DEFAULT = 244
    TRY = 245
    CATCH = 246
    FINALLY = 247
    THROW = 248


    # ==========================
    # Function Operations (260-289)
    # ==========================

    CALL = 260
    RETURN = 261
    CALL_NATIVE = 262
    CALL_ASYNC = 263
    YIELD = 264
    LAMBDA = 265
    CLOSURE = 266
    BIND = 267
    APPLY = 268
    CALL_THIS = 269
    PARTIAL = 270
    MEMOIZE = 271


    # ==========================
    # Class/Object Operations (290-319)
    # ==========================

    CLASS_DEF = 290
    CLASS_EXTENDS = 291
    NEW = 292
    DELETE = 293
    GET_PROP = 294
    SET_PROP = 295
    GET_PROTO = 296
    SET_PROTO = 297
    HAS_PROP = 298
    DEL_PROP = 299
    KEYS = 300
    VALUES = 301
    ENTRIES = 302
    INSTANCEOF = 303
    THIS = 304
    SUPER = 305
    STATIC = 306


    # ==========================
    # I/O Operations (320-349)
    # ==========================

    PRINT = 320
    PRINTLN = 321
    INPUT = 322
    READ_FILE = 323
    WRITE_FILE = 324
    APPEND_FILE = 325
    DELETE_FILE = 326
    FILE_EXISTS = 327
    FILE_SIZE = 328
    FILE_COPY = 329
    FILE_RENAME = 330
    FILE_MOVE = 331
    DIR_CREATE = 332
    DIR_EXISTS = 333
    DIR_LIST = 334
    DIR_DELETE = 335
    PATH_JOIN = 336
    PATH_DIRNAME = 337
    PATH_BASENAME = 338
    PATH_EXTNAME = 339
    GET_STDIN = 340
    GET_STDOUT = 341
    GET_STDERR = 342
    FLUSH = 343


    # ==========================
    # System Operations (350-379)
    # ==========================

    EXIT = 350
    HALT = 351
    SLEEP = 352
    TIME = 353
    DATE = 354
    TIMESTAMP = 355
    RANDOM = 356
    RANDOM_INT = 357
    RANDOM_RANGE = 358
    SEED = 359
    ENV_GET = 360
    ENV_SET = 361
    ENV_DEL = 362
    ARGV = 363
    GETPID = 364
    GETPPID = 365
    FORK = 366
    EXEC = 367
    SYSTEM = 368
    VERSION = 369
    PLATFORM = 370
    ARCH = 371


    # ==========================
    # Exception/Error (380-399)
    # ==========================

    THROW_ERROR = 380
    TRY_CATCH = 381
    FINALLY_BLOCK = 382
    ERROR_HANDLER = 383
    ASSERT = 384
    WARN = 385
    DEBUG = 386
    ERROR = 387


    # ==========================
    # Advanced Features (400-429)
    # ==========================

    ASYNC_CALL = 400
    AWAIT = 401
    PROMISE = 402
    THEN = 403
    CATCH_PROMISE = 404
    GENERATOR = 405
    NEXT = 406
    ITERATOR = 407
    ITERABLE = 408
    ENUM = 409
    STRUCT = 410
    UNION = 411
    PATTERN_MATCH = 412
    DESTRUCTURE = 413
    SPREAD = 414
    REST = 415


    # ==========================
    # Regex Operations (430-439)
    # ==========================

    REGEX_COMPILE = 430
    REGEX_MATCH = 431
    REGEX_SEARCH = 432
    REGEX_REPLACE = 433
    REGEX_SPLIT = 434
    REGEX_TEST = 435


    # ==========================
    # Hash Operations (440-449)
    # ==========================

    HASH = 440
    MD5 = 441
    SHA1 = 442
    SHA256 = 443
    SHA512 = 444
    BASE64_ENCODE = 445
    BASE64_DECODE = 446
    HEX_ENCODE = 447
    HEX_DECODE = 448


    # ==========================
    # JSON Operations (450-459)
    # ==========================

    JSON_PARSE = 450
    JSON_STRINGIFY = 451
    JSON_PRETTY = 452
    YAML_PARSE = 453
    YAML_STRINGIFY = 454


    # ==========================
    # Date/Time Operations (460-469)
    # ==========================

    DATE_NEW = 460
    DATE_NOW = 461
    DATE_FORMAT = 462
    DATE_PARSE = 463
    DATE_ADD = 464
    DATE_SUB = 465
    DATE_DIFF = 466
    TIMEZONE = 467
    LOCALE = 468


    # ==========================
    # Debug Operations (470-479)
    # ==========================

    DEBUG_PRINT = 470
    DEBUG_TRACE = 471
    DEBUG_BREAK = 472
    DEBUG_ASSERT = 473
    DEBUG_PROFILE = 474
    DEBUG_MEMORY = 475
    DEBUG_STACK = 476
    DEBUG_VARS = 477
    DISASM = 478
    DUMP = 479


    # ==========================
    # Miscellaneous (480-499)
    # ==========================

    NOP = 480
    NOOP = 481
    RESERVED = 482
    PLUGIN_CALL = 483
    EXTENSION = 484
    VERSION_CHECK = 485
    FEATURE_CHECK = 486
    PRAGMA = 487
    INLINE = 488


    # ==========================
    # Termination (500)
    # ==========================

    HALT_VM = 500


    # ==========================
    # Debug Lookup Table
    # ==========================

    _NAMES = {
        # Stack
        1: "PUSH", 2: "POP", 3: "DUP", 4: "SWAP", 5: "ROT", 6: "OVER", 7: "DEPTH", 8: "CLEAR_STACK",

        # Memory
        10: "STORE", 11: "LOAD", 12: "STORE_GLOBAL", 13: "LOAD_GLOBAL", 14: "STORE_LOCAL", 15: "LOAD_LOCAL",
        16: "ALLOC", 17: "FREE", 18: "COPY_MEMORY", 19: "ZERO_MEMORY", 20: "MOVE_MEMORY", 21: "HEAP_PUSH",
        22: "HEAP_POP", 23: "HEAP_PEEK", 24: "SET_REF", 25: "GET_REF",

        # Arithmetic
        30: "ADD", 31: "SUB", 32: "MUL", 33: "DIV", 34: "MOD", 35: "POWER", 36: "NEG", 37: "ABS",
        38: "SQRT", 39: "EXP", 40: "LN", 41: "LOG", 42: "LOG10", 43: "SIN", 44: "COS", 45: "TAN",
        46: "ASIN", 47: "ACOS", 48: "ATAN", 49: "FLOOR", 50: "CEIL", 51: "ROUND", 52: "TRUNC",
        53: "MAX", 54: "MIN", 55: "CLAMP", 56: "SIGN", 57: "FAC",

        # Comparison
        60: "EQ", 61: "NE", 62: "LT", 63: "LE", 64: "GT", 65: "GE", 66: "CMP", 67: "ISNULL",
        68: "ISNOTNULL", 69: "ISNAN", 70: "ISINF",

        # Logical
        80: "AND", 81: "OR", 82: "NOT", 83: "XOR", 84: "NAND", 85: "NOR", 86: "XNOR",

        # Bitwise
        100: "BITAND", 101: "BITOR", 102: "BITXOR", 103: "BITNOT", 104: "LSHIFT", 105: "RSHIFT",
        106: "ARSHIFT", 107: "ROTL", 108: "ROTR", 109: "POPCOUNT", 110: "CLZA", 111: "CTZB",

        # String
        120: "STR_PUSH", 121: "STR_POP", 122: "STR_CONCAT", 123: "STR_LEN", 124: "STR_SUBSTR",
        125: "STR_FIND", 126: "STR_REPLACE", 127: "STR_UPPER", 128: "STR_LOWER", 129: "STR_TRIM",
        130: "STR_SPLIT", 131: "STR_JOIN", 132: "STR_COMPARE", 133: "STR_STARTSWITH", 134: "STR_ENDSWITH",
        135: "STR_CONTAINS", 136: "STR_INDEX", 137: "STR_REVERSE", 138: "STR_REPEAT", 139: "STR_FORMAT",
        140: "STR_ENCODE", 141: "STR_DECODE", 142: "CHAR_CODE", 143: "CODE_CHAR",

        # Array
        150: "ARRAY_NEW", 151: "ARRAY_GET", 152: "ARRAY_SET", 153: "ARRAY_PUSH", 154: "ARRAY_POP",
        155: "ARRAY_LEN", 156: "ARRAY_SHIFT", 157: "ARRAY_UNSHIFT", 158: "ARRAY_SLICE", 159: "ARRAY_SPLICE",
        160: "ARRAY_CONCAT", 161: "ARRAY_REVERSE", 162: "ARRAY_SORT", 163: "ARRAY_FIND", 164: "ARRAY_FINDINDEX",
        165: "ARRAY_INCLUDES", 166: "ARRAY_INDEXOF", 167: "ARRAY_LASTINDEXOF", 168: "ARRAY_MAP", 169: "ARRAY_FILTER",
        170: "ARRAY_REDUCE", 171: "ARRAY_FOREACH", 172: "ARRAY_FILL", 173: "ARRAY_COPY", 174: "ARRAY_CLEAR",
        175: "ARRAY_REMOVE", 176: "ARRAY_INSERT", 177: "ARRAY_SUM", 178: "ARRAY_AVG", 179: "ARRAY_MAX",
        180: "ARRAY_MIN", 181: "ARRAY_ALL", 182: "ARRAY_ANY", 183: "ARRAY_UNIQUE", 184: "ARRAY_FLAT",
        185: "ARRAY_CHUNK", 186: "ARRAY_ZIP",

        # Map
        190: "MAP_NEW", 191: "MAP_SET", 192: "MAP_GET", 193: "MAP_DEL", 194: "MAP_HAS",
        195: "MAP_KEYS", 196: "MAP_VALUES", 197: "MAP_SIZE", 198: "MAP_CLEAR", 199: "MAP_COPY",
        200: "MAP_MERGE",

        # Type
        210: "TYPE_OF", 211: "TYPE_CHECK", 212: "CAST_INT", 213: "CAST_FLOAT", 214: "CAST_STR",
        215: "CAST_BOOL", 216: "CAST_ARRAY", 217: "CAST_MAP", 218: "IS_INT", 219: "IS_FLOAT",
        220: "IS_STR", 221: "IS_BOOL", 222: "IS_ARRAY", 223: "IS_MAP", 224: "IS_CALLABLE",
        225: "IS_NUMERIC",

        # Control Flow
        230: "JMP", 231: "JMP_IF_TRUE", 232: "JMP_IF_FALSE", 233: "JMP_IF_NULL", 234: "JMP_IF_NOTNULL",
        235: "LABEL", 236: "COND_JMP", 237: "LOOP", 238: "LOOP_WHILE", 239: "LOOP_UNTIL",
        240: "BREAK", 241: "CONTINUE", 242: "CASE", 243: "SWITCH", 244: "DEFAULT",
        245: "TRY", 246: "CATCH", 247: "FINALLY", 248: "THROW",

        # Function
        260: "CALL", 261: "RETURN", 262: "CALL_NATIVE", 263: "CALL_ASYNC", 264: "YIELD",
        265: "LAMBDA", 266: "CLOSURE", 267: "BIND", 268: "APPLY", 269: "CALL_THIS",
        270: "PARTIAL", 271: "MEMOIZE",

        # Class/Object
        290: "CLASS_DEF", 291: "CLASS_EXTENDS", 292: "NEW", 293: "DELETE", 294: "GET_PROP",
        295: "SET_PROP", 296: "GET_PROTO", 297: "SET_PROTO", 298: "HAS_PROP", 299: "DEL_PROP",
        300: "KEYS", 301: "VALUES", 302: "ENTRIES", 303: "INSTANCEOF", 304: "THIS", 305: "SUPER",
        306: "STATIC",

        # I/O
        320: "PRINT", 321: "PRINTLN", 322: "INPUT", 323: "READ_FILE", 324: "WRITE_FILE",
        325: "APPEND_FILE", 326: "DELETE_FILE", 327: "FILE_EXISTS", 328: "FILE_SIZE", 329: "FILE_COPY",
        330: "FILE_RENAME", 331: "FILE_MOVE", 332: "DIR_CREATE", 333: "DIR_EXISTS", 334: "DIR_LIST",
        335: "DIR_DELETE", 336: "PATH_JOIN", 337: "PATH_DIRNAME", 338: "PATH_BASENAME", 339: "PATH_EXTNAME",
        340: "GET_STDIN", 341: "GET_STDOUT", 342: "GET_STDERR", 343: "FLUSH",

        # System
        350: "EXIT", 351: "HALT", 352: "SLEEP", 353: "TIME", 354: "DATE", 355: "TIMESTAMP",
        356: "RANDOM", 357: "RANDOM_INT", 358: "RANDOM_RANGE", 359: "SEED", 360: "ENV_GET",
        361: "ENV_SET", 362: "ENV_DEL", 363: "ARGV", 364: "GETPID", 365: "GETPPID", 366: "FORK",
        367: "EXEC", 368: "SYSTEM", 369: "VERSION", 370: "PLATFORM", 371: "ARCH",

        # Exception
        380: "THROW_ERROR", 381: "TRY_CATCH", 382: "FINALLY_BLOCK", 383: "ERROR_HANDLER",
        384: "ASSERT", 385: "WARN", 386: "DEBUG", 387: "ERROR",

        # Advanced
        400: "ASYNC_CALL", 401: "AWAIT", 402: "PROMISE", 403: "THEN", 404: "CATCH_PROMISE",
        405: "GENERATOR", 406: "NEXT", 407: "ITERATOR", 408: "ITERABLE", 409: "ENUM",
        410: "STRUCT", 411: "UNION", 412: "PATTERN_MATCH", 413: "DESTRUCTURE", 414: "SPREAD",
        415: "REST",

        # Regex
        430: "REGEX_COMPILE", 431: "REGEX_MATCH", 432: "REGEX_SEARCH", 433: "REGEX_REPLACE",
        434: "REGEX_SPLIT", 435: "REGEX_TEST",

        # Hash
        440: "HASH", 441: "MD5", 442: "SHA1", 443: "SHA256", 444: "SHA512",
        445: "BASE64_ENCODE", 446: "BASE64_DECODE", 447: "HEX_ENCODE", 448: "HEX_DECODE",

        # JSON
        450: "JSON_PARSE", 451: "JSON_STRINGIFY", 452: "JSON_PRETTY", 453: "YAML_PARSE", 454: "YAML_STRINGIFY",

        # Date/Time
        460: "DATE_NEW", 461: "DATE_NOW", 462: "DATE_FORMAT", 463: "DATE_PARSE", 464: "DATE_ADD",
        465: "DATE_SUB", 466: "DATE_DIFF", 467: "TIMEZONE", 468: "LOCALE",

        # Debug
        470: "DEBUG_PRINT", 471: "DEBUG_TRACE", 472: "DEBUG_BREAK", 473: "DEBUG_ASSERT",
        474: "DEBUG_PROFILE", 475: "DEBUG_MEMORY", 476: "DEBUG_STACK", 477: "DEBUG_VARS",
        478: "DISASM", 479: "DUMP",

        # Misc
        480: "NOP", 481: "NOOP", 482: "RESERVED", 483: "PLUGIN_CALL", 484: "EXTENSION",
        485: "VERSION_CHECK", 486: "FEATURE_CHECK", 487: "PRAGMA", 488: "INLINE",

        # Termination
        500: "HALT_VM",
    }

    @staticmethod
    def name(code):
        return OpCode._NAMES.get(code, "UNKNOWN")


# Built-in operation IDs.  They are deliberately stable because .zbc files
# store the numeric ID rather than a Python object or string.
NATIVE_IDS = {
    name: i + 1 for i, name in enumerate([
        "ADD","SUB","MUL","DIV","MOD","POWER","MAX","MIN","CLAMP",
        "ABS","SQRT","EXP","LN","LOG","LOG10","SIN","COS","TAN","ASIN","ACOS","ATAN",
        "FLOOR","CEIL","ROUND","TRUNC","SIGN","FAC",
        "EQ","NE","LT","LE","GT","GE","AND","OR","NOT","XOR","NAND","NOR","XNOR",
        "BITAND","BITOR","BITXOR","BITNOT","LSHIFT","RSHIFT","ARSHIFT","ROTL","ROTR","POPCOUNT",
        "STR","TEXT","CHAR","JOIN","CUT","SLICE","SUBSTR","REPLACE","UPPER","LOWER","TRIM","SPACE",
        "FORMAT","CONCAT","PARSE","ENCODE","DECODE","COUNTCHAR","STARTSWITH","ENDSWITH","CONTAINS",
        "REVERSE","REPEAT","SPLIT","FINDSTR","MATCHSTR","TOSTRING",
        "LIST","PUSH","POP","INSERT","DELETEAT","GETAT","SETAT","FIRST","LAST","SIZE","LENGTH",
        "SORT","FILTER","REDUCE","MERGE","FLATTEN","FLAT","UNIQUE","FIND","FINDINDEX","INCLUDES",
        "INDEXOF","SHIFT","UNSHIFT","SPLICE","FILL","COPY",
        "KEYS","VALUES","ENTRIES","HAS","PROPERTY","PROP",
        "TYPE_OF","TYPEOF","IS","INT","FLOAT","BOOL","STRINGIFY","NUMBER","DATE","TIME","INSTANCE",
        "EMPTY","VALID","INVALID","CONVERT","AUTO",
        "FILE_READ","FILE_WRITE","FILE_APPEND","FILE_EXISTS","FILE_SIZE","FILE_DELETE","FILE_COPY","FILE_MOVE",
        "DIR_CREATE","DIR_EXISTS","DIR_LIST","DIR_DELETE","PATH",
        "ENV","ARGV","GETPID","GETPPID","SLEEP","TIMESTAMP","SEED","RANDOM","VERSION","SYSTEM","SYSTEMOS",
        "PLATFORM","ARCH",
        "HASH","MD5","SHA","SHA1","SHA256","SHA512","BASE64","ENCODE64","DECODE64","HEX",
        "JSON","YAML","PARSE_JSON","STRINGIFY_JSON",
        "REGEX","PATTERN","MATCH","ENUM","STRUCT","UNION","GENERATOR","NEXT","ITERATOR",
        "DESTRUCTURE","SPREAD","REST","PROMISE","THEN","ASYNC","AWAIT",
        "ASSERT","DEBUG","WARN","ERROR","DUMP","DISASM","NOP","NOOP"
    ])
}
# Runtime helpers that are language keywords rather than legacy built-ins.
# Appended IDs preserve the existing .zbc native IDs.
for _extra_name in [
    "NEW", "THIS", "SUPER", "STATIC", "EXTENDS", "CLASS", "CAST", "OUT", "IN",
    "TRUE", "FALSE", "NULL", "VOID", "MATH", "STRING", "ARRAY", "MAP", "OBJECT",
    "SWITCH", "CASE", "DEFAULT", "BREAK", "CONTINUE", "WHEN", "ELSE", "END",
]:
    if _extra_name not in NATIVE_IDS:
        NATIVE_IDS[_extra_name] = max(NATIVE_IDS.values(), default=0) + 1

NATIVE_NAMES = {v: k for k, v in NATIVE_IDS.items()}
