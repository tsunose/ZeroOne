"""Compatibility VM entry point.

The canonical runtime lives in :mod:`vm.vm`.  This module keeps the original
file layout/API while avoiding two diverging virtual machines.
"""
from vm.vm import ZeroOneVM

VirtualMachine = ZeroOneVM

__all__ = ["ZeroOneVM", "VirtualMachine"]
