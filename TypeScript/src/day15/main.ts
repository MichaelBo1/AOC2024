import fs from "fs";

enum Entities {
    Box = "O",
    Robot = "@",
    Wall = "#",
    Space = ".",
}

enum Moves {
    Up = "^",
    Down = "v",
    Left = "<",
    Right = ">",
}

interface Position {
    row: number
    col: number
}

function parseGrid(rawGrid: string): Entities[][] {
    return rawGrid.split("\n").map(row => 
        row.split("").map(char => {
            switch (char) {
                case Entities.Box:
                    return Entities.Box;
                case Entities.Robot:
                    return Entities.Robot;
                case Entities.Wall:
                    return Entities.Wall;
                case Entities.Space:
                    return Entities.Space;
                default:
                    throw new Error(`Invalid entity character: ${char}`);
            }
        })
    );
}

function parseMoves(movesSeq: string): Moves[] {
    return movesSeq.replace(/(\r\n|\n|\r)/gm, "").split("").map(char => {
        switch (char) {
            case Moves.Up:
                return Moves.Up;
            case Moves.Down:
                return Moves.Down;
            case Moves.Left:
                return Moves.Left;
            case Moves.Right:
                return Moves.Right;
            default:
                console.log(char.charCodeAt(0))
                throw new Error(`invalid move character: ${char}`)
        }
    });
}

function nextPosition(pos: Position, move: Moves): Position {
    switch (move) {
        case Moves.Up: return {row: pos.row - 1, col: pos.col};
        case Moves.Down: return {row: pos.row + 1, col: pos.col};
        case Moves.Left: return {row: pos.row, col: pos.col - 1};
        case Moves.Right: return {row: pos.row, col: pos.col + 1};
    }
}

function findRobot(grid: Entities[][]): Position {
    for (let row = 0; row < grid.length; row++) {
        for (let col = 0; col < grid[row].length; col++) {
            if (grid[row][col] === Entities.Robot) {
                return { row, col };
            }
        }
    }
    throw new Error("Robot not found in the grid!");
}


function moveRobot(grid: Entities[][], robotPos: Position, move: Moves): Position {
    function getLine(start: Position, move: Moves): Position[] {
        const line: Position[] = [start];
        let currentPos = nextPosition(start, move);
    
        while (currentPos.row >= 0 && currentPos.row < grid.length && currentPos.col >= 0 && currentPos.col < grid[0].length) {
            const entity = grid[currentPos.row][currentPos.col];
            if (entity === Entities.Wall) break;
            line.push(currentPos);

            if (entity === Entities.Space) break;
            currentPos = nextPosition(currentPos, move);
        }
        return line;
    }

    function shiftLine(line: Position[]) {
        for (let i = line.length - 1; i > 0; i--) {
            const current = line[i];
            const prev = line[i-1];
            grid[current.row][current.col] = grid[prev.row][prev.col];
        }
        const start = line[0];
        grid[start.row][start.col] = Entities.Space;
    }

    const line = getLine(robotPos, move);
    const hasSpace = line.some(pos => grid[pos.row][pos.col] === Entities.Space)
    if (line.length <= 1 || !hasSpace) return robotPos;

    shiftLine(line);
    return nextPosition(robotPos, move);
}

function gridToString(grid: Entities[][]): string {
    return grid.map(row => row.join("")).join("\n");
}

function part1(grid: Entities[][], moves: Moves[]): number {
    let robotPos = findRobot(grid);
    // console.log(gridToString(grid), "\n")
    for (const move of moves) {
        robotPos = moveRobot(grid, robotPos, move);
        // console.log(`Move: ${move}`)
        // console.log(gridToString(grid), "\n")
    }
    
    let result = 0;
    const rows = grid.length;
    const cols = grid[0].length;
    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
            if (grid[row][col] === Entities.Box) {
                result += 100 * row + col;
            }
        }
    }
    return result;
}

const EXAMPLE = `########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
`

const EXAMPLE_LARGE = `##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^`

let raw: string;
if (process.argv.length == 3) {
    const filepath = process.argv[2];
    raw = fs.readFileSync(filepath, "utf-8")
} else {
    raw = EXAMPLE_LARGE;
}

const parts = raw.split("\n\n");
const grid = parseGrid(parts[0]);
const moves = parseMoves(parts[1])

console.log(`Part 1: ${part1(grid, moves)}`);


