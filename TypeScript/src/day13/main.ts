import fs from "fs";

const BUTTON_A_COST = 3;
const BUTTON_B_COST = 1;
// For part 2
const CONVERSION_CORRECTION = 10000000000000;

interface Position {
    x: number
    y: number
}
interface Machine {
    buttonA: Position
    buttonB: Position
    prize: Position
}
interface Solution {
    aPresses: number
    bPresses: number
}

function parseMachines(input: string): Machine[] {
    const machines: Machine[] = [];
    const matchPattern = /Button A: X\+(\d+), Y\+(\d+)\s*Button B: X\+(\d+), Y\+(\d+)\s*Prize: X=(\d+), Y=(\d+)/g;

    let match
    while ((match = matchPattern.exec(input)) !== null ) {
        const [_, aX, aY, bX, bY, pX, pY] = match.map(Number)

        machines.push({
            buttonA: { x: aX, y: aY },
            buttonB: { x: bX, y: bY },
            prize: { x: pX, y: pY }
        });
    }
    return machines;
}

// Solving 2x2 by Cramer's
// https://danceswithcode.net/engineeringnotes/linear_equations/linear_equations.html

function determinant(matrix: number[][]): number {
    return matrix[0][0]*matrix[1][1] - matrix[1][0]*matrix[0][1]
}

function solveMachine(machine: Machine): Solution {
    const numA = determinant([
        [machine.prize.x, machine.buttonB.x],
        [machine.prize.y, machine.buttonB.y]
    ])
    const denomA = determinant([
        [machine.buttonA.x, machine.buttonB.x],
        [machine.buttonA.y, machine.buttonB.y]
    ])
    if (denomA === 0) {
        throw new Error("zero division")
    }
    let aPresses = numA / denomA;
    let bPresses = (machine.prize.x - machine.buttonA.x*aPresses) / machine.buttonB.x
    
    // We disregard if not properly solved
    if (!Number.isInteger(aPresses) || !Number.isInteger(bPresses)) {
        aPresses = 0;
        bPresses = 0;
    }
    return {aPresses, bPresses};
}

function tokensToPlay(machines: Machine[], correction: boolean): number {
    if (correction) {
        machines = machines.map((machine) => {
        return {
            buttonA: machine.buttonA,
            buttonB: machine.buttonB,
            prize: {
                x: machine.prize.x + CONVERSION_CORRECTION,
                y: machine.prize.y + CONVERSION_CORRECTION,
            },
        };
    });
    }
    return machines.map((machine) => solveMachine(machine))
        .map(sol => sol.aPresses * BUTTON_A_COST + sol.bPresses * BUTTON_B_COST)
        .reduce((acc, value) => acc + value, 0);
}

const EXAMPLE = `Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
`

const EXAMPLE_LARGE = `Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
`

let raw: string;
if (process.argv.length == 3) {
    const filepath = process.argv[2];
    raw = fs.readFileSync(filepath, "utf-8")
} else {
    // raw = EXAMPLE;
    raw = EXAMPLE_LARGE;
}

const machines = parseMachines(raw);
console.log(`Part 1: ${tokensToPlay(machines, false)}`);
console.log(`Part 2: ${tokensToPlay(machines, true)}`)