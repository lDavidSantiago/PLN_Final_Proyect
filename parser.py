# Parser (top-down)
"""
->  Start in S
->  we test the first symbol of the input string against the first symbol
    for each production rule for S. If it matches, we consume the symbol and move to the next symbol 
    in the input string. If it doesn't match, we backtrack and try the next production rule for S.
-> If a production fails, we fall back and try next production rule for the previous non-terminal.
-> If none work we report an error.


"""

from grammar import build_cfg
from tree import TreeNode

#-------------- if error is found, we raise this exception --------------#
class ParseError(Exception):
    def __init__(self,message,pos=None,tokens=None):
        self.pos = pos
        self.tokens = tokens or []
        super().__init__(message)
    
    def show_error(self):
        if self.tokens and self.pos is not None:
            seen = [f"'{t.valor}'" for t in self.tokens[:self.pos]]
            not_seen = [f"'{t.valor}'" for t in self.tokens[self.pos:]]
            
            if seen:
                print("Seen: " + " ".join(seen))
            if not_seen:
                print("Not seen: " + " ".join(not_seen))
        print(f"Error: {self.args[0]}")


#------------------ The main parser class ------------------#
class Parser:
    
    def __init__(self,cfg=None):
        self.cfg = cfg or build_cfg()
        self.tokens = []
        self._pos = 0
        
    def parse(self, tokens):
        # ? Args needed to start -> tokens: list of tokens to parse
        
        self.tokens = tokens
        self._pos = 0
        
        if not self.tokens:
            raise ParseError("No tokens to parse.")
        
        
        # We start the parsing process by trying to derive the start symbol (S) using its production rules.
        # If any of the production rules for S successfully derives the input tokens, we return the resulting parse tree.
        # If none of the production rules for S can derive the input tokens, we raise a ParseError
        
        
        last_error = None
        for prod in self.cfg.get_productions(self.cfg.S):
            result = self._parse_production(prod,0)
            if result is not None:
                node,final_pos = result
                if final_pos == len(tokens):
                    return node
                else:
                    last_error = ParseError(
                        f"Error sintactico: se esperaba el fin de entrada, "
                        f"pero se encontraron tokens adicionales a partir de la posicion {final_pos + 1}.",
                        pos=final_pos, tokens=self.tokens
                    )

        if last_error is not None:
            raise last_error

        raise ParseError(
            "Error sintactico: la entrada no coincide con ninguna produccion de S.",
            pos=0, tokens=self.tokens
        )
            
            
#----------------------------- Methods for parsing variables and productions -----------------------------#



    def _parse_variable(self, variable, pos):
        """
        Try to parse the no terminal `variable` starting from position `pos` in the token list.
        trys all the productions for `variable` and returns the first successful parse result.
        if none of the productions work, raises a ParseError with a descriptive message.
        """
        productions = self.cfg.get_productions(variable)

        if not productions:
            raise ParseError(
                f"Error interno: la variable '{variable}' no tiene producciones.",
                pos=pos, tokens=self.tokens
            )

        for prod in productions:
            result = self._parse_production(prod, pos)
            if result is not None:
                return result

        # None of them worked, we report an error with the current token
        tok_desc = (f"'{self.tokens[pos].valor}'" if pos < len(self.tokens)
                    else "fin de entrada")
        raise ParseError(
            f"Error sintactico: no se puede derivar '{variable}' "
            f"con el token {tok_desc} en la posicion {pos + 1}.",
            pos=pos, tokens=self.tokens
        )

    
    

    def _parse_production(self, prod, pos):
        """
        After we got the productions we want to try this functions iterate for each of them,
        finding the first one that can successfully parse the input tokens starting from position `pos`.
        
        """
        nodo      = TreeNode(prod.left, production=prod)
        pos_actual = pos

        for symbol in prod.right:
            """
                Non-terminals -> {'S', 'CMD_COMP', 'CMD', 'OBJ', 'DEST'}
                Terminals     -> {'VERBS', 'DET', 'TYPE', 'PREP', 'CONNECTOR', 'EXT', 'NAMED_AS', 'NAMING'}
            """
            
            if self.cfg.is_terminal(symbol):
                #  If its a terminal, we check if the current token matches the expected terminal 
                # symbol.
                # if its non terminal we call recursively to _parse_variable to try to parse it and 
                # add the resulting subtree as a child of the current node.
                if pos_actual >= len(self.tokens):
                    return None   

                tok = self.tokens[pos_actual]
                if tok.tipo != symbol:
                    return None   

                # Create a leaf node for the matched terminal symbol 
                hoja = TreeNode(symbol, token=tok)
                nodo.add_child(hoja)
                pos_actual += 1

            else:
                # ── Recursion ──────────────────────────────
                try:
                    hijo, pos_actual = self._parse_variable(symbol, pos_actual)
                    nodo.add_child(hijo)
                except ParseError:
                    return None   
        # Return production node and the position after parsing this production
        return (nodo, pos_actual)
