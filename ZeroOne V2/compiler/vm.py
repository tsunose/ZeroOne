"""Compatibility wrapper for the VM implementation."""

from vm.vm import ZeroOneVM


class VirtualMachine(ZeroOneVM):
    """Backward-compatible interface expected by the entrypoint scripts."""

    def execute(self, opcode=None, operand=None):
        if opcode is None and operand is None:
            self.run()
            return

        return super().execute(opcode, operand)


__all__ = ["ZeroOneVM", "VirtualMachine"]
