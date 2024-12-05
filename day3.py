from __future__ import annotations
from typing import Callable, Optional

file = open('data/day3.txt').read().splitlines()

class State:
    '''A state stores its transition states and the symbols that
    lead to them.'''
    def __init__(self, name: str) -> None:
        self.name = name
        self.transitions = dict()
    
    def add_transition(self, symbol: str, state: State) -> None:
        '''Add a transition state.'''
        self.transitions[symbol] = state

    def can_transition(self, symbol: str) -> bool:
        '''Check whether the symbol leads to a transition state.'''
        return symbol in self.transitions
    
    def transition(self, symbol: str) -> State:
        '''Return the transition state that corresponds to the given symbol.'''
        return self.transitions[symbol]

# Create states for each symbol in the string 'mul(x1[x2][x3],y1[y2][y3])', with
# states x2, x3, y2 and y3 as optional states.

state_start = State('start')
state_m = State('m')
state_u = State('u')
state_l = State('l')
state_pl_mul = State('mul (')
state_x1 = State('x1')
state_x2 = State('x2')
state_x3 = State('x3')
state_comma = State(',')
state_y1 = State('y1')
state_y2 = State('y2')
state_y3 = State('y3')
state_pr_mul = State('mul )')

# Add transitions
state_start.add_transition('m', state_m)
state_m.add_transition('u', state_u)
state_u.add_transition('l', state_l)
state_l.add_transition('(', state_pl_mul)

# Add all transitions that has a digit as symbol
for i in range(0, 10):
    n = str(i)
    state_pl_mul.add_transition(n, state_x1)
    state_x1.add_transition(n, state_x2)
    state_x2.add_transition(n, state_x3)
    state_comma.add_transition(n, state_y1)
    state_y1.add_transition(n, state_y2)
    state_y2.add_transition(n, state_y3)

# Add transitions for the digits
state_x1.add_transition(',', state_comma)
state_x2.add_transition(',', state_comma)
state_x3.add_transition(',', state_comma)

state_y1.add_transition(')', state_pr_mul)
state_y2.add_transition(')', state_pr_mul)
state_y3.add_transition(')', state_pr_mul)

# Lookup sets to see if we need to convert the symbol into a number
x_states = { state_x1, state_x2, state_x3 }
y_states = { state_y1, state_y2, state_y3 }

# Initialize the state machine
current_state = state_start
x, y = 0, 0
result = 0

for line in file:
    for char in line:
        if current_state.can_transition(char):
            # State can transition
            current_state = current_state.transition(char)
            
            if current_state in x_states:
                # Add digit to x
                x = 10 * x + int(char)
            
            elif current_state in y_states:
                # Add digit to y
                y = 10 * y + int(char)
            
            elif current_state is state_pr_mul:
                # Final state for mul(x,y). Add to result and set state to start state.
                result += x * y
                x, y = 0, 0
                current_state = state_start
        
        else:
            x, y = 0, 0
            current_state = state_start

print(result)

#  Create the states for do() and don't()
state_d = State('d')
state_o = State('o')
state_pl_do = State('do (')
state_pr_do = State('do )')
state_n = State('n')
state_apos = State("'")
state_t = State('t')
state_pl_dont = State("don't (")
state_pr_dont = State("don't )")

# Add the transitions
state_start.add_transition('d', state_d)
state_d.add_transition('o', state_o)

state_o.add_transition('(', state_pl_do)
state_pl_do.add_transition(')', state_pr_do)

state_o.add_transition('n', state_n)
state_n.add_transition("'", state_apos)
state_apos.add_transition('t', state_t)
state_t.add_transition('(', state_pl_dont)
state_pl_dont.add_transition(')', state_pr_dont)

# Initialize the state machine
current_state = state_start
x, y = 0, 0
result = 0
do_mul = True

for line in file:
    for char in line:
        if current_state.can_transition(char):
            # State can transition
            current_state = current_state.transition(char)
            
            if current_state in x_states:
                # Add digit to x
                x = 10 * x + int(char)
            
            elif current_state in y_states:
                # Add digit to y
                y = 10 * y + int(char)
            
            elif current_state is state_pr_do:
                # End state for do()
                do_mul = True
                current_state = state_start
            
            elif current_state is state_pr_dont:
                # End state for don't()
                do_mul = False
                current_state = state_start
            
            elif current_state is state_pr_mul:
                # End state for mul(x,y). Add product to result if do() was the last command.
                if do_mul:
                    result += x * y
                
                # Reset state to start state
                x, y = 0, 0
                current_state = state_start
        
        else:
            # Unknown transition, go to start state
            x, y = 0, 0
            current_state = state_start
    
print(result)