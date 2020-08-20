# Simple Turing Machines

## Busy Beaver
Busy beavers as implemented here are turing machines which run on a 1-dimensional tape.
The tape is initialized with 0 and the turing machine reads and writes to the tape as per its set of instructions.
<br>
Given an initial 'state' and a current position, the instruction set for each state tells the machine 
what to write, where to move next and which state (and thus instruction set) to move to next.
Implmented here are 2 'colours' that they can be written to the tape (I.e 0 or 1).
The script generalizes to any number of states.

<br>
Each state is associated with a set of instructions, encapsulated by the Card Class.
I.e:

card = Card(1, "112", "102")  
where 1 indicated the state id; on which to call execute these instructions  
"112" is the instruction set for the case where the underlying value at the position is 0  
"102" is the instruction set for the case where the underlying value at the position is 1  
"112" instructs the machine to:  
	write 1 to the position,   
	move right ("1" for right, "0" for left),  
	go to card for state 2  

The process stops once card 0 - the "Halt" state is reached.   
The interesting part of this is in considering the domain of programs which can be coded 
by these simple rules. Do all of them reach the halt state? Do some continue forever?  
Is there any way to determine if one these machines halts or goes forever?
<br>
These questions motivate the busy beaver game:
Given an n number of states, determine the instruction set which gives the maximum number of sequential '1's at the end halt state.
Such a Turing Machine is deemed the BB-n  Turing Machine.
<br><br>

The busy_beaver script is a simple implementation written in python. [1, 2, 3]
Might write a C++ version in the future, but not really neccessary unless the script
is extended to perform a search (I.e as in the Zany Zoo [4])

Requirements:
python 3

<br><br>

## Turmite
A 2d version of the Busy Beaver formulation, this one is more fun as the visual patterns
that emerge on 2-d graphs are more interesting than the 1d bb machines.
The script runs some standard machines which can be found at [5].
The instruction sets for the given machines are in turmites.json along with a reccommended number ot iterations to run for. (As they don't have a halt state and will run forever).

Some Examples:
<br>
![snowflake](/examples/snowflake.png)
![spiral](/examples/spiral.png)
![fractal](/examples/fractal.png)
![highway](/examples/highway.png)
![barcode](/examples/barcode.png)


Requirements:
numpy == 1.18.1 (most versions should be fine)
matplotlib == 3.1.3 (most versions should be fine)

## TODO
	- Find new turmites
	- Rewrite BB in C++ and consider implementing Zany Zoo (much pre-reading required)



![1. Busy Beaver Wiki](https://en.wikipedia.org/wiki/Busy_beaver)  
![2. Aaronson, S. The Busy Beaver Frontier.](https://www.scottaaronson.com/papers/bb.pdf)  
![3. Numberphile Video](https://www.youtube.com/watch?v=CE8UhcyJS0I)  
![4. Harland, J. (2016). Generating Candidate Busy Beaver Machines (Or How to Build the Zany Zoo). arXiv preprint arXiv:1610.03184.](https://arxiv.org/abs/1610.03184)  
![5. Turmite Wiki](https://en.wikipedia.org/wiki/Turmite)  

