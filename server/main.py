from .routes import app
from puzzlesolver.puzzles import PuzzleManager

import os

from threading import Thread

app.config["DEBUG"] = False
app.config["TESTING"] = False
app.config['DATABASE_DIR'] = 'databases'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Start server
def server_start(app, host=None, part=None, solve=True):
    t = Thread(target=app.run, kwargs={"host" : host, "port" : port})
    t.start()
    if solve:
        init_data()

# Initalizes the data
def init_data():
    for p_cls in PuzzleManager.getPuzzleClasses():        
        if app.config["TESTING"]:
            variants = p_cls.test_variants
        else:
            variants = p_cls.variants
        for variant in variants:
            s_cls = PuzzleManager.getSolverClass(p_cls.id, variant)
            puzzle = p_cls.generateStartPosition(variant)
            solver = s_cls(puzzle, dir_path=app.config['DATABASE_DIR'])
            solver.solve(verbose=True)


if __name__ == "__main__":
    host, port = '127.0.0.1', 9001
    if 'GMP_HOST' in os.environ:
        host = os.environ['GMP_HOST']
    if 'GMP_PORT' in os.environ:
        port = os.environ['GMP_PORT']
    server_start(app, host, port, True)
