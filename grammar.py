from pprint import pformat

# 
# Gramatica de Contexto Libre
#
#
# V : conjunto de variables (no terminales)
# T : conjunto de terminales -- son los TIPOS de token que produce el lexer
# P : conjunto de producciones (reglas)
# S : simbolo inicial
#

# --- Produccion ---------------------------------------------------------------


class Production:
    """
    @param __init__: Class constructor for Production objects.
    @param prod_id: A unique identifier for the production rule.    
    @param left: The left-hand side of the production rule, which is a non-terminal 
    symbol.
    @param right: The right-hand side of the production rule, which is a list of 
    symbols (terminals and/or non-terminals).
    
    
    @param __repr__: A method that returns a string representation of the Production (Like a print)
    
    @param length: A method that returns the number of symbols on the right-hand side of 
    the production rule.
    """
    def __init__(self, prod_id, left, right):
        self.id = prod_id
        self.left = left
        self.right = right
        
    def __repr__(self):
        return f"{self.id}: {self.left} -> {' '.join(self.right)}"

    def length(self):
        return len(self.right)
    

class CFG:
    # G = (V, T, P, S)
    def __init__(self, variables,terminals,productions,start_symbol):
        self.V = variables
        self.T = terminals
        self.P = productions
        self.S = start_symbol
        
        
        # Build and index for productions so we dont have to 
        # iterate evertime we want to find productions for a 
        # variable
        
        self._index = {}
        for prod in self.P:
            variable = prod.left
            
            if variable not in self._index:
                self._index[variable] = []
            self._index[variable].append(prod)
    
    def get_productions(self, variable):
        return self._index.get(variable, [])
    
    def is_terminal(self, symbol):
        return symbol in self.T
    
    def is_variable(self, symbol):
        return symbol in self.V
    
    
    def show(self):
        sep = "-" * 30
        productions = [(prod.id, prod.left, " ".join(prod.right)) for prod in self.P]
        id_width = max(len("ID"), *(len(prod_id) for prod_id, _, _ in productions))
        left_width = max(len("Left"), *(len(left) for _, left, _ in productions))
        right_width = max(len("Right"), *(len(right) for _, _, right in productions))
        row_sep = f"  +-{'-' * id_width}-+-{'-' * left_width}-+-{'-' * right_width}-+"

        print(sep)
        print("  CFG")
        print("  G = (V, T, P, S)")
        print(sep)
        print(f"  S = {self.S}  (start symbol)")
        print()
        print("  V =")
        print(pformat(sorted(self.V), indent=4, width=68))
        print()
        print("  T =")
        print(pformat(sorted(self.T), indent=4, width=68))
        print()
        print("  P = productions:")
        print(row_sep)
        print(f"  | {'ID':<{id_width}} | {'Left':<{left_width}} | {'Right':<{right_width}} |")
        print(row_sep)
        for prod_id, left, right in productions:
            print(f"  | {prod_id:<{id_width}} | {left:<{left_width}} | {right:<{right_width}} |")
        print(row_sep)
        print(sep)
    
def build_cfg():
    """
    Builds and returns a context-free grammar (CFG) 
    
    Variables (V):
        S        -> start symbol -> sentence
        CMD_COMP -> 2 commands (verbs,actions) connected by a connector (and, then, etc)
        CMD      -> simple command -> verb + object + Optional[destination]
        OBJ -> object -> determiner + type + Optional[extension/name]
        DEST -> destination/target phrase     
    
    Terminals (T):
        VERBS | DET | TYPE | PREP | CONNECTOR | EXT | NAMED_AS | NAMING | 
    
    Productions (P):
        P1:  S        -> CMD
        P2:  S        -> CMD_COMP
        P3:  CMD_COMP -> CMD CONNECTOR CMD
        P4:  CMD      -> VERBS OBJ
        P5:  CMD      -> VERBS OBJ DEST
        P6:  OBJ      -> DET TYPE
        P7:  OBJ      -> DET TYPE EXT
        P8:  OBJ      -> DET TYPE NAMING
        P9:  OBJ      -> DET TYPE NAMED_AS NAMING
        P10: OBJ      -> DET TYPE EXT NAMED_AS NAMING
        P11: DEST     -> PREP NAMING
        P12: DEST     -> NAMED_AS NAMING
        P13: DEST     -> NAMING
    """
    
    variables = {'S', 'CMD_COMP', 'CMD', 'OBJ', 'DEST'}
    terminals = {'VERBS', 'DET', 'TYPE', 'PREP', 'CONNECTOR', 'EXT', 'NAMED_AS', 'NAMING'}
    productions = [
        #P1:  S        -> CMD
        Production('P1', 'S', ['CMD']),
        #P2:  S        -> CMD_COMP
        Production('P2', 'S', ['CMD_COMP']),
        #P3:  CMD_COMP -> CMD CONNECTOR CMD
        Production('P3', 'CMD_COMP', ['CMD', 'CONNECTOR', 'CMD']),
        #P5:  CMD      -> VERBS OBJ DEST WHY? Longest match first
        Production('P5', 'CMD', ['VERBS', 'OBJ', 'DEST']),
        #P4:  CMD      -> VERBS OBJ
        Production('P4', 'CMD', ['VERBS', 'OBJ']),
        #P10: OBJ      -> DET TYPE EXT NAMED_AS NAMING
        Production('P10', 'OBJ', ['DET', 'TYPE', 'EXT', 'NAMED_AS', 'NAMING']),
        #P9:  OBJ      -> DET TYPE NAMED_AS NAMING
        Production('P9', 'OBJ', ['DET', 'TYPE', 'NAMED_AS', 'NAMING']),
        #P8:  OBJ      -> DET TYPE NAMING
        Production('P8', 'OBJ', ['DET', 'TYPE', 'NAMING']),
        #P7:  OBJ      -> DET TYPE EXT
        Production('P7', 'OBJ', ['DET', 'TYPE', 'EXT']),
        #P6:  OBJ      -> DET TYPE
        Production('P6', 'OBJ', ['DET', 'TYPE']),
        #P11: DEST     -> PREP NAMING
        Production('P11', 'DEST', ['PREP', 'NAMING']),
        #P12: DEST     -> NAMED_AS NAMING
        Production('P12', 'DEST', ['NAMED_AS', 'NAMING']),
        #P13: DEST     -> NAMING
        Production('P13', 'DEST', ['NAMING']),   
    ]
    
    return CFG(
        variables    = variables,
        terminals    = terminals,
        productions  = productions,
        start_symbol = 'S',
    )
    

# --------------- TEST ----------------------
if __name__ == '__main__':
    cfg = build_cfg()
    cfg.show()
