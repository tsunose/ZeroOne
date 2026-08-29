"""ZeroOne command line interface - V2.0.2"""
import argparse
import os
import sys
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.assembler import Assembler
from compiler.bytecode import ByteCodeWriter, ByteCodeReader
from vm.vm import ZeroOneVM

VERSION = "2.0.2"

def read_source(filename):
    with open(filename, "r", encoding="utf-8") as f: return f.read()

def compile_source(source):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    intermediate = Generator().generate(ast)
    return Assembler().assemble(intermediate)

def compile_file(filename, output=None):
    if not filename.endswith(".zo"): raise ValueError("Only .zo files are allowed.")
    code = compile_source(read_source(filename))
    output = output or os.path.splitext(filename)[0] + ".zbc"
    writer = ByteCodeWriter()
    for inst in code: writer.add_instruction(inst[0], inst[1] if len(inst)>1 else 0)
    writer.save(output)
    print(f"Compiled: {filename} -> {output}")
    return output

def run_file(filename):
    data = ByteCodeReader().load(filename)
    vm = ZeroOneVM()
    vm.load(data["instructions"])
    vm.run()
    return vm

def run_source(filename):
    code = compile_source(read_source(filename))
    vm = ZeroOneVM(); vm.load(code); vm.run(); return vm

def main(argv=None):
    parser = argparse.ArgumentParser(prog="zo", description="ZeroOne compiler / VM")
    parser.add_argument("--version", action="version", version=f"ZeroOne {VERSION}")
    sub = parser.add_subparsers(dest="command")
    c = sub.add_parser("compile"); c.add_argument("source"); c.add_argument("-o","--output")
    r = sub.add_parser("run"); r.add_argument("bytecode")
    s = sub.add_parser("run-source"); s.add_argument("source")
    args = parser.parse_args(argv)
    if args.command == "compile": compile_file(args.source,args.output)
    elif args.command == "run": run_file(args.bytecode)
    elif args.command == "run-source": run_source(args.source)
    else: parser.print_help()

if __name__ == "__main__": main()
