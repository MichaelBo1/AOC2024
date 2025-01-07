import fs, { write } from "fs";

interface Vector2D {
    x: number
    y: number
}

interface Robot {
    position: Vector2D
    velocity: Vector2D
}

function parseRobots(input: string): Robot[] {
    const robots: Robot[] = [];
    const pattern = /p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)/g

    let match
    while ((match = pattern.exec(input)) !== null ) {
        const [_, pX, pY, vX, vY] = match.map(Number)

        robots.push({
            position: {x: pX, y: pY},
            velocity: {x: vX, y: vY}
        });
    }
    return robots;
}

function createGrid(robots: Robot[], maxX: number, maxY: number): string {
    const grid: string[][] = Array.from({ length: maxY }, () => Array(maxX).fill("."));
    for (const robot of robots) {
        const {x, y} = robot.position;
        grid[y][x] = "#"
    }

    return grid.map((row) => row.join("")).join("\n");
}

function simulateRobots(robots: Robot[], nIterations: number, maxX: number, maxY: number): Robot[] {
    for (let i = 0; i < nIterations; i++) {
       let j = 0;
        for (let robot of robots) {
            const nextPosition = {
                x: robot.position.x + robot.velocity.x,
                y: robot.position.y + robot.velocity.y,
            }
            // Wrap to keep in bounds if necessary
            if (nextPosition.x < 0) {
                nextPosition.x += maxX;
            }
            if (nextPosition.x >= maxX) {
                nextPosition.x %= maxX;
            }
            if (nextPosition.y < 0) {
                nextPosition.y += maxY;
            }
            if (nextPosition.y >= maxY) {
                nextPosition.y %= maxY;
            }
            robot.position = nextPosition
            
        }
    }

    return robots
}

function countAndMultiply(quadrants: number[]): number {
    const initialCounts = [0,0,0,0]

    const counts = quadrants.reduce((acc, num) => {
        if (num >= 1 && num <= 4) {
            acc[num-1]++;
        }
        return acc;
    }, initialCounts)
    
    return counts.reduce((acc, val) => acc * val, 1);
}

function computeSafety(robots: Robot[], maxX: number, maxY: number) {
    const midX = Math.floor(maxX / 2);
    const midY = Math.floor(maxY / 2);

    function getQuadrant(pos: Vector2D): number {
        let quad = 0;
        if (pos.x == midX || pos.y == midY) {
            return quad;
        }
        if (pos.x < midX) {
            quad += 1;
        } else if (pos.x > midX) {
            quad += 3;
        }
        if (pos.y > midY) {
            quad += 1;
        }
        return quad;
    }

    const quadrants = robots.map(robot => getQuadrant(robot.position)).filter(quad => quad > 0);
    return countAndMultiply(quadrants);
}

const EXAMPLE = `p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
`

const nIterations = 100;
let raw: string;
let maxX;
let maxY;

if (process.argv.length == 3) {
    const filepath = process.argv[2];
    raw = fs.readFileSync(filepath, "utf-8")
    maxX = 101;
    maxY = 103;
} else {
    raw = EXAMPLE;
    maxX = 11;
    maxY = 7;
}

const robots = parseRobots(raw);
// Part 1
const simulated1 = simulateRobots(robots, nIterations, maxX, maxY)
const result1 = computeSafety(simulated1, maxX, maxY);
console.log(`Part 1: ${result1}`)
