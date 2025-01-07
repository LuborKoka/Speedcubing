from fastapi.templating import Jinja2Templates


TEMPLATES = Jinja2Templates(directory="./app/view")
CUBES = [
    {'size': 2, 'puzzle': '2x2x2', 'status': 'inactive'},
    {'size': 3, 'puzzle': '3x3x3', 'status': 'inactive'},
    {'size': 4, 'puzzle': '4x4x4', 'status': 'inactive'},
    {'size': 5, 'puzzle': '5x5x5', 'status': 'inactive'},
    {'size': 6, 'puzzle': '6x6x6', 'status': 'dead'},
    {'size': 7, 'puzzle': '7x7x7', 'status': 'dead'},
    {'size': 8, 'puzzle': '8x8x8', 'status': 'dead'},
    {'size': 9, 'puzzle': '9x9x9', 'status': 'inactive'}
]

PUZZLES = ['2x2x2', '3x3x3', '4x4x4', '5x5x5', '6x6x6', '7x7x7', '8x8x8', '9x9x9']

WCA_SCRAMBLE_LENGTHS = {
    '2x2x2': 11,
    '3x3x3': 20,
    '4x4x4': 40,
    '5x5x5': 60,
    '6x6x6': 80,
    '7x7x7': 100,
    '8x8x8': 120,
    '9x9x9': 140
}

OPPOSITE_FACES = {
    'R': 'L', 'L': 'R',
    'U': 'D', 'D': 'U',
    'F': 'B', 'B': 'F'
}

MODIFIERS = ['', "'", '2']
MOVES = ['R', 'L', 'U', 'D', 'F', 'B']