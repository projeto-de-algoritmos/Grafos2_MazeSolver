from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from lab import generate_maze, bfs


app = Flask(__name__)
CORS(app)

@app.route('/generate_maze', methods=['POST'])
def generate():
    size = request.json.get('size', 10)
    start, end, maze = generate_maze(size)
    return jsonify({'start': start, 'end': end, 'maze': maze.tolist()})

@app.route('/solve_maze', methods=['POST'])
def solve():
    maze = np.array(request.json['maze'])
    start = tuple(request.json['start'])
    end = tuple(request.json['end'])
    path = bfs(maze, start, end)
    return jsonify({'path': path})

if __name__ == '__main__':
    import webbrowser

    webbrowser.open_new("http://localhost:3000")
    app.run(host='localhost')
