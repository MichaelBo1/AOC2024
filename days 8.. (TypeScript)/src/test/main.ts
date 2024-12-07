import fs from "fs";

if (process.argv.length < 3) {
    console.error('Please provide a file path');
    process.exit(1);
}

const filePath = process.argv[2];
const content = fs.readFileSync(filePath, 'utf8');
console.log(content.split("\n"));