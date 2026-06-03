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
        '''
        self.Q      = set(states)          # states
        self.sigma  = set(alphabet)        # alphabet
        self.delta  = transitions     # dict: {(state, symbol): next_state} δ : Q × Σ → Q
        self.q0     = initial_state   # initial state
        self.F      = set(final_states)    # final states
        self._state = initial_state   # current state
        self.show()  # show the DFA definition for verification


    def reset(self):
        '''This function resets the automaton to the initial state.'''
        self._state = self.q0

    def transition(self, symbol):
        self._state = self.delta.get((self._state, symbol), 'q_error')
        return self._state
    def accepting(self):
        return self._state in self.F

    def current_state(self):
        return self._state

    def process(self, sequence):
        self.reset()
        for symbol in sequence:
            self.transition(symbol)
        return self.accepting()
    
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
    states = {'q0','q0','q_hola','q_adios','q_error'}
    alphabet = {'hola','adios'}
    transitions = {
        ('q0','hola'):'q_hola',
        ('q0','adios'):'q_adios',
        }
    dfa = DFA(states, alphabet, transitions, initial_state='q0', final_states={'q_hola','q_adios'})

    print(dfa.process(['hola']))    # True
    print(dfa.process(['otro']))    # False
    print(dfa.process(['adios']))   # True
    print(dfa.Q)
test1()
