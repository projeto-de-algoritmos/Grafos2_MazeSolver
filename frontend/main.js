const mazeSizeInput = document.getElementById('maze-size');
const generateMazeButton = document.getElementById('generate-maze');
const solveMazeButton = document.getElementById('solve-maze');
const mazeContainer = document.getElementById('maze-container');

const apiBaseUrl = 'http://localhost:5000';


function renderMaze(maze, start, end) {
    mazeContainer.innerHTML = '';

    for (let y = 0; y < maze.length; y++) {
        for (let x = 0; x < maze[y].length; x++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');

            if (maze[y][x] === 1) {
                cell.style.backgroundColor = 'black';
            }

            if (y === start[0] && x === start[1]) {
                cell.classList.add('start');
            } else if (y === end[0] && x === end[1]) {
                cell.classList.add('end');
            }

            cell.addEventListener('click', () => {
                maze[y][x] = maze[y][x] === 1 ? 0 : 1;
                renderMaze(maze, start, end);
            });

            mazeContainer.appendChild(cell);
        }

        mazeContainer.appendChild(document.createElement('br'));
    }
}


function renderPath(path) {
    if (!path) {
        alert('Não tem Solução!');
        return;
    }

    const cells = mazeContainer.getElementsByClassName('cell');
    for (const [y, x] of path.slice(1, -1)) {
        const index = y * mazeSizeInput.value + x;
        cells[index].classList.add('path');
    }
}

async function generateMaze() {
    const size = parseInt(mazeSizeInput.value);
    const response = await fetch(`${apiBaseUrl}/generate_maze`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ size: size })
    });

    const data = await response.json();
    renderMaze(data.maze, data.start, data.end);
    return { maze: data.maze, start: data.start, end: data.end };
}

async function solveMaze(maze, start, end) {
    const response = await fetch(`${apiBaseUrl}/solve_maze`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ maze: maze, start: start, end: end })
    });

    const data = await response.json();
    renderPath(data.path);
    
}

generateMazeButton.addEventListener('click', async () => {
    const { maze, start, end } = await generateMaze();
    solveMazeButton.onclick = () => solveMaze(maze, start, end);
});
