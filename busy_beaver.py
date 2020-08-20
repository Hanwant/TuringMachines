#!/home/hemu/miniconda3/envs/madigan/bin/python3.7

from collections.abc import MutableMapping
from array import array

class Tape(MutableMapping):
    def __init__(self, init=20):
        self.tape = array('b', [0 for i in range(init)])

    def __len__(self):
        return len(self.tape)

    def __repr__(self):
        return repr(['-' if num == 0 else '■' for num in self.tape])
        # return repr(self.tape)

    def __getitem__(self, item):
        """
        Takes care of boundary conditions extending tape in either direction if attempt to read new memory is made
        Assume moves of no more than 1 shift in either left or right direction
        """
        if item == -1:
            self.tape = array('b', [0]) + self.tape
            return self.tape[0]
        elif item == len(self):
            self.tape.append(0)
            return self.tape[-1]
        return self.tape[item]

    def __delitem__(self, item):
        raise NotImplemented("deletion of tape memory is prohibited")

    def __iter__(self):
        return iter(self.tape)

    def __setitem__(self, item, value):
        self.tape[item] = value

class Card:
    def __init__(self, number, row1, row2):
        assert len(row1) == 3 and len(row2) == 3, "length of input strings must be 3 each"
        self.halt = False
        self.n = number
        self.a0 = int(row1[0])
        self.b0 = int(row1[1])
        self.c0 = int(row1[2])
        self.a1 = int(row2[0])
        self.b1 = int(row2[1])
        self.c1 = int(row2[2])

class HaltCard(Card):
    def __init__(self):
        super().__init__(0, "000", "000")
        self.halt=True


class TuringMachine:
    def __init__(self, cards, start_pos=0):
        self.cards = {card.n: card for card in [HaltCard()]+cards}
        self.pos = start_pos
        self.cur_card = self.cards[1]

    def move(self, b):
        if b is 0:
            return -1
        elif b is 1:
            return 1

    def read(self, tape):
        inp = tape[self.pos]
        if self.pos == -1: # To be consistent with python indexing
            self.pos = 0
        if inp is 0:
            tape[self.pos] = self.cur_card.a0
            self.pos += self.move(self.cur_card.b0)
            self.cur_card = self.cards[self.cur_card.c0]
        elif inp is 1:
            tape[self.pos] = self.cur_card.a1
            self.pos += self.move(self.cur_card.b1)
            self.cur_card = self.cards[self.cur_card.c1]
        if self.cur_card.halt:
            raise StopIteration("Halt")


if __name__ == "__main__":
    tape = Tape(10)
    start_pos = 4
    c0 = HaltCard()
    two_stateA = [
        Card(1,
             "112",
             "102"
        ),
        Card(2,
             "101",
             "110"
        )
    ]
    three_stateA = [
        Card(1,
             "112",
             "110"
        ),
        Card(2,
             "013",
             "112"
        ),
        Card(3,
             "103",
             "101"
        )
    ]
    beaver = TuringMachine(three_stateA, start_pos = start_pos)
    LIMIT = 15
    try:
        i = 0
        while True:
            i += 1
            # import ipdb; ipdb.set_trace()
            print(tape)
            beaver.read(tape)
            if i > LIMIT:
                raise StopIteration(f"Ran for over {LIMIT} steps; terminating")
    except StopIteration as E:
        print(E)
        print("steps: ", i, "score: ", sum(tape))

