import fs from "fs";
import { Op, OpCodeMap, OpToInstruction, Registers } from "./instructions";

class Computer {
    registers: Registers;
    instructionMap: OpCodeMap;
    pc: number;
    result: string[];

    constructor(registers: Registers, instructionMap: OpCodeMap) {
        this.registers = registers;
        this.instructionMap = instructionMap;
        this.pc = 0;
        this.result = [];
    }

    run(program: Op[]) {
        while (this.pc < program.length) {
            const opCode = program[this.pc];
            const operand = program[this.pc+1];

            const instructionFn = this.instructionMap[opCode];
            const {registers, pcState, output} = instructionFn({registers: this.registers, operand: operand, pc: this.pc});

            this.registers = registers;
            this.pc = pcState;
            if (output !== undefined) this.result.push(output.toString());
        }
        }

    printResult() {
        console.log(this.result.join(","));
    }

}

function parseRegisters(input: string): Registers {
    const regA = Number(input.match(/Register A: (\d+)/)?.[1] || 0);
    const regB = Number(input.match(/Register B: (\d+)/)?.[1] || 0);
    const regC = Number(input.match(/Register C: (\d+)/)?.[1] || 0);
    return {regA, regB, regC};
}

function parseProgram(programStr: string): Op[] {
    const parts = programStr.split(" ");
    const ops = parts[1]
        .split(",")
        .map(str => Number(str))
        .filter((num): num is Op => num >= 0 && num <= 7);
    return ops;
}

const EXAMPLE = `Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
`
const PUZZLE = `Register A: 17323786
Register B: 0
Register C: 0

Program: 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
`

const USE_PUZZLE = true;
let raw: string;

if (USE_PUZZLE) {
    raw = PUZZLE;
} else {
    raw = EXAMPLE;
}

const parts = raw.trim().split("\n\n");
const registers = parseRegisters(parts[0])
const program = parseProgram(parts[1])
const computer = new Computer(registers, OpToInstruction);
// const test = {
//     regA: 2024,
//     regB: 0,
//     regC: 0,
// }
// const computer = new Computer(test, OpToInstruction);
// console.log(computer.registers)
// computer.run([0,1,5,4,3,0])
// console.log(computer.registers)
// computer.printResult()

console.log("Running:")
computer.run(program);
computer.printResult();
