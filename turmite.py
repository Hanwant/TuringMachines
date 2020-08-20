#!/home/hemu/miniconda3/envs/madigan/bin/python3.7

from collections.abc import MutableMapping
from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np


def cast(x, dtype):
    """
    Convenience function to cast to numpy types
    numpy chosen for fine grained control over memory usage I.e uint8 vs int
    """
    return np.array(x, dtype=dtype).item()

def load_json(path, set_id):
    """
    path: path to json file
    state_typeL I.e 2State, 3State
    set_id: unique id for each set of turmite programs
    """
    with open(path, 'r') as f:
        data = json.load(f)
        state_set = data[set_id]["states"]
        num_iter = data[set_id]["iterations"]
    states = []
    for k, v in state_set.items():
        colours = []
        for _, c in v.items():
            colours.append(c)
        states.append(State(int(k), *colours))
    return states, num_iter


class Tape(MutableMapping):
    def __init__(self, init=20, dtype = np.bool):

        """
        init: init size of square grid
        dtype: np.bool for binary colours, np.uint8 for small number of colours
               np.int for larger number of colours
        """
        self.dtype = dtype
        self.tape = np.zeros((init, init), dtype = self.dtype)

    @property
    def shape(self):
        return self.tape.shape

    def __len__(self):
        return len(self.tape)

    def __repr__(self):
        # return repr(self.tape)
        out = np.zeros(self.shape, dtype = str)
        out[self.tape == 0] = ' '
        out[self.tape == 1] = '■' # '⬤'
        return str(out).replace("'", "").replace("[[", " ").replace("]]", " ").replace("[", "").replace("]", "")

    @property
    def new_row(self):
        return np.zeros((1, self.shape[1]), self.dtype)

    @property
    def new_col(self):
        return np.zeros((self.shape[0], 1), self.dtype)


    def __getitem__(self, item):
        """
        Takes care of boundary conditions extending tape in either direction if attempt to read new memory is made
        Assume moves of no more than 1 shift in either left or right direction
        """
        assert len(item) == 2, "Must specify x and y co-ordinates"
        x, y = item
        if x == -1:
            self.tape = np.concatenate([self.new_row, self.tape], axis=0)
            x = 0
        elif x == self.shape[0]:
            self.tape = np.concatenate([self.tape, self.new_row], axis=0)
        if y == -1:
            self.tape = np.concatenate([self.new_col, self.tape], axis=1)
            y = 0
        elif y == self.shape[1]:
            self.tape = np.concatenate([self.tape, self.new_col], axis=1)
        return self.tape[x, y]

    def __delitem__(self, item):
        raise NotImplemented("deletion of tape memory is prohibited")

    def __iter__(self):
        return iter(self.tape)

    def __setitem__(self, item, value):
        self.tape[item[0], item[1]] = value


class State:
    def __init__(self, number, *colours, dtype = bool):
        # assert len(row1) == 3 and len(row2) == 3, "length of input strings must be 3 each"
        self.halt = False
        self._n = number
        self._colours = {dtype(int(colour[0])): {'c': colour[1], 't': colour[2], 'n': colour[3]} for colour in colours}
        assert len(self._colours) == len(colours), f"Duplicate state rules passed, parsed: {len(colours)}, {len(self._colours)}"

    @property
    def n(self):
        return self._n

    def __getitem__(self, item):
        return self._colours[item]

    def items(self):
        return self._colours.items()

    def __repr__(self):
        return f"<TurmiteState>{self.n}"


class HaltState(State):
    def __init__(self):
        super().__init__(0, "00N0", "10N0")
        self.halt=True

class Orientation:
    def __init__(self, pos=0):
        self.i = pos
        self.states = ('N', 'E', 'S', 'W')
        self.o = self.states[self.i]

    @property
    def state(self):
        return self.states[self.i]

    def __add__(self, rotate):
        if rotate == 'R':
            self.i = (self.i + 1) % 4
        elif rotate == 'L':
            self.i = (self.i - 1) % 4
        elif rotate == 'U':
            self.i = (self.i + 2) % 4
        elif rotate == 'N':
            pass
        else:
            raise KeyError('Incorrect rotation command')
        return self

    def __repr__(self):
        return self.state

    def __str__(self):
        return repr(self)

class Turmite:
    """
    2 Colors
    """
    def __init__(self, states, start_pos=[0, 0], dtype = np.bool):
        self.states = {state.n: state for state in states}
        for state in self.states.values():
            for color, rule in state.items():
                rule['c'] = dtype(int(rule['c']))
                rule['n'] = int(rule['n'])

        self.pos = start_pos
        self.orientation = Orientation()
        self.cur_state = self.states[0]
        self.tape = Tape(5, dtype = dtype)

    def move(self, rotate):
        self.orientation += rotate
        if self.orientation.state == 'N':
            self.pos[0] += -1
        elif self.orientation.state == 'E':
            self.pos[1] += 1
        elif self.orientation.state == 'S':
            self.pos[0] += 1
        elif self.orientation.state == 'W':
            self.pos[1] += -1
        else:
            raise ValueError("rotation not valid: ", rotate)

    def crawl(self):
        inp = self.tape[self.pos]
        if self.pos[0] == -1: # To be consistent with python indexing
            self.pos[0] = 0
        if self.pos[1] == -1: # To be consistent with python indexing
            self.pos[1] = 0
        self.tape[self.pos] = self.cur_state[inp]['c']
        self.move(self.cur_state[inp]['t'])
        self.cur_state = self.states[self.cur_state[inp]['n']]
        if self.cur_state.halt:
            raise StopIteration("Halt")


def main(name = "a", filepath = "turmites.json", PRINT=True, PLOT=True):

    states, num_iter = load_json(filepath, name)

    if len(states) == 2:
        dtype = np.bool
    elif 2 < len(states) <= 255:
        dtype = np.uint32
    else:
        dtype = np.int

    turmite = Turmite(states, dtype=dtype)
    tape = turmite.tape
    LIMIT = num_iter
    try:
        i = 0
        print(tape, '\n')
        while True:
            i += 1
            turmite.crawl()
            if PRINT:
                print(tape, '\n', ''.join(['--' for i in range(tape.shape[1])]))
            if i > LIMIT:
                raise StopIteration(f"Ran for over {LIMIT} steps; terminating")
    except StopIteration as E:
        print(E)
        print("steps: ", i, "score: ", np.sum(tape))
        if PLOT:
            plt.imshow(tape, cmap='binary')
            plt.axis('off')
            plt.show()


if __name__ == "__main__":
    main("box", PRINT=False, PLOT=True)
