export type Op = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;
export interface Registers {
    regA: number;
    regB: number;
    regC: number;
}

export type InstructionResult = {registers: Registers, pcState: number, output?: number}
export type IntructionHandler = (args: {registers: Registers; operand: Op, pc: number}) => InstructionResult;
export type OpCodeMap = {
    [key in Op]: IntructionHandler;
}

function comboOperand(operand: Op, registers: Registers): number {
    if (operand >= 0 && operand <= 3) {
        return operand;
    }
    if (operand === 4) return registers.regA;
    if (operand === 5) return registers.regB;
    if (operand === 6) return registers.regC;
    return operand;
}

const instructionAdvance: IntructionHandler = ({registers, operand, pc}) => {
    const num = registers.regA;
    const combo = comboOperand(operand, registers);
    const denom = Math.pow(2, combo);
    registers.regA = Math.trunc(num / denom);
    return {registers: registers, pcState: pc + 2};
}

export const instructionBitwiseXORLiteral: IntructionHandler = ({registers, operand, pc}) => {
    registers.regB = registers.regB ^ operand;
    return {registers: registers, pcState: pc + 2};
}

export const instructionMod: IntructionHandler = ({registers, operand, pc}) => {
    const combo = comboOperand(operand, registers)
    registers.regB = combo % 8;
    return {registers: registers, pcState: pc + 2};
}

export const instructionJumpNotZero: IntructionHandler = ({registers, operand, pc}) => {
    if (registers.regA === 0) return {registers: registers, pcState: pc + 2};
    return {registers: registers, pcState: operand};
}

export const instructionBitwiseXOR: IntructionHandler = ({registers, operand, pc}) => {
    registers.regB = registers.regB ^ registers.regC;
    return {registers: registers, pcState: pc + 2};
}

export const instructionOutput: IntructionHandler = ({registers, operand, pc}) => {
    const value = comboOperand(operand, registers) % 8;
    return {registers: registers, pcState: pc + 2, output: value};
}

export const instructionBAdvance: IntructionHandler = ({registers, operand, pc}) => {
    const num = registers.regA;
    const combo = comboOperand(operand, registers);
    const denom = Math.pow(2, combo);
    registers.regB = Math.trunc(num / denom);
    return {registers: registers, pcState: pc + 2};
}

export const instructionCAdvance: IntructionHandler = ({registers, operand, pc}) => {
    const num = registers.regA;
    const combo = comboOperand(operand, registers);
    const denom = Math.pow(2, combo);
    registers.regC = Math.trunc(num / denom);
    return {registers: registers, pcState: pc + 2};
}

export const OpToInstruction: OpCodeMap = {
    0: instructionAdvance,
    1: instructionBitwiseXORLiteral,
    2: instructionMod,
    3: instructionJumpNotZero,
    4: instructionBitwiseXOR,
    5: instructionOutput,
    6: instructionBAdvance,
    7: instructionCAdvance,
}