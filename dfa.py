class DFA: 

    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        '''    
        # we declare the class DFA(Deterministic Finite Automaton  with the following attributes:
        # Q: set of states
        # Σ(sigma): input alphabet
        # δ(delta): transition function
        # q0: initial state
        # F: set of accepting states
        # set help us to ensure that states and alphabet are unique and to easily check membership
        # we also define a trap state q_error for undefined transitions and add it to the set of states
        '''
        self.Q      = set(states)          # states
        self.sigma  = set(alphabet)        # alphabet
        self.delta  = transitions     # dict: {(state, symbol): next_state} δ : Q × Σ → Q
        self.q0     = initial_state   # initial state
        self.F      = set(final_states)    # final states
        self._state = initial_state   # current state
        self.q_error = 'q_error'      # trap state for undefined transitions
        self.Q.add(self.q_error)       # add trap state to the set of states\
        # validate the DFA definition is well-formed
        # q0 in Q, F subset of Q, transitions defined for all states and symbols
        self._validate()         
        self.show()  # show the DFA definition for verification
        #self._complete_error_state()  # ensure all undefined transitions go to q_error
        self._state = self.q0  # start at the initial state

    def _validate(self):
        '''Validate the DFA definition is well-formed.'''
        if self.q0 not in self.Q:# check initial state is in Q
            raise ValueError(f"Initial state q0 '{self.q0}' must be in the set of states Q.")
        
        # all transitions must be defined for states in Q
        if not self.F.issubset(self.Q):# check final states are subset of Q, issubset is a method of set that checks if F is a subset of Q
            #{1,2}.issubset({1,2,3}) → True
            #{1,4}.issubset({1,2,3}) → False
            raise ValueError(f"Final states F {self.F} must be a subset of the set of states Q.")
        # now, we check all the transitions in delta
        for (state, symbol), next_state in self.delta.items():
            # check that the state, symbol, and next_state are valid
            if state not in self.Q:
                raise ValueError(f"Transition state '{state}' is not in the set of states Q.")
            # check that the symbol is in the alphabet and the next state is in Q
            if symbol not in self.sigma:
                raise ValueError(f"Transition symbol '{symbol}' is not in the alphabet Σ.")
            # check that the next state is in Q
            if next_state not in self.Q:
                raise ValueError(f"Transition next state '{next_state}' is not in the set of states Q.")

    def process(self, sequence):
        """Process sequence; return True if accepted."""
        self._state = self.q0  # start at initial
        for symbol in sequence:  # apply transitions
            if (self._state, symbol) in self.delta:
                self._state = self.delta[(self._state, symbol)]
            else:
                self._state = self.q_error  # undefined -> trap
        return self._state in self.F  # True if in accepting states

    # we define the method reset to reset the automaton to the initial state
    #def reset(self):


    def show(self):
        '''Shows the automaton definition in a readable format.'''
        print("DFA Definition:")
        print(f"States (Q): {self.Q}")
        print(f"Alphabet (Σ): {self.sigma}")
        print(f"Initial State (q0): {self.q0}")
        print(f"Final States (F): {self.F}")
        print("Transitions (δ):")
        for (state, symbol), next_state in self.delta.items():
            print(f"  δ({state}, {symbol}) = {next_state}")


def test1():
    states = {'q0','q_hola','q_adios','q_error'}
    alphabet = {'hola','adios'}
    transitions = {
        ('q0','hola'):'q_hola',
        ('q0','adios'):'q_adios',
        }
    dfa = DFA(states, alphabet, transitions, initial_state='q0', final_states={'q_hola','q_adios'})

    print(dfa.process(['hola']))    # True
    print(dfa.process(['otro']))    # False -> va a 'q_error'
    print(dfa.process(['adios']))   # True
test1()
