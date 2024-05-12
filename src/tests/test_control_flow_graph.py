#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import random
import unittest
from art.framework.backend.control_flow.control_flow_graph import ControlFlowGraph
from art.framework.backend.ir.code import Code
from art.framework.backend.ir.operation_code import OperationCode
from art.framework.backend.ir.quadruple import Quadruple


class Test(unittest.TestCase):
    @staticmethod
    def generate_code(n):
        opcodes = [OperationCode.MIR_NOOP,
                   OperationCode.MIR_IF_TRUE,
                   OperationCode.MIR_IF_FALSE,
                   OperationCode.MIR_GOTO,
                   OperationCode.MIR_RETURN]
        code = Code()
        k = 1
        for i in range(n):
            opcode = random.choice(opcodes)
            if opcode == OperationCode.MIR_NOOP:
                instruction = Quadruple(k + 0, operation=opcode)
                code.instructions.append(instruction)
                instruction = Quadruple(k + 1, operation=opcode)
                code.instructions.append(instruction)
                instruction = Quadruple(k + 2, operation=opcode)
                code.instructions.append(instruction)
                k += 3
            else:
                instruction = Quadruple(k, operation=opcode)
                code.instructions.append(instruction)
                k += 1
        return code

    def test_cfg_collect_basic_blocks_success(self):
        cfg = ControlFlowGraph()
        code = Test.generate_code(16)
        print(code)
        bb = cfg.collect_basic_blocks(code)
        assert True


if __name__ == '__main__':
    """
    """
    unittest.main()
