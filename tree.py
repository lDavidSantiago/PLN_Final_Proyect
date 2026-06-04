# tree.py
# Derivation tree for the recursive descent parser.
# Interior nodes = CFG variables, leaves = terminals (with their Token).

class TreeNode:
    """
    Node of a derivation tree.

    Interior node : label=variable, children=[TreeNode], production=Production
    Leaf node     : label=token_type, children=[], token=Token
    """

    def __init__(self, label, token=None, production=None):
        self.label      = label
        self.token      = token
        self.production = production
        self.children   = []

    def add_child(self, node):
        self.children.append(node)

    def is_leaf(self):
        return len(self.children) == 0

    def yield_tokens(self):
        """Returns the list of leaf tokens left-to-right (frontier of the tree)."""
        if self.is_leaf() and self.token is not None:
            return [self.token]
        result = []
        for child in self.children:
            result.extend(child.yield_tokens())
        return result

    # ── Visual representation ──────────────────────────────────────────────

    def _leaf_desc(self):
        if self.token.valor != self.token.valor_norm:
            return f"{self.label}  '{self.token.valor}' ({self.token.valor_norm})"
        return f"{self.label}  '{self.token.valor}'"

    def __str__(self):
        lines = []
        if self.production is not None:
            lines.append(f"{self.label}  [{self.production.id}]")
        elif self.token is not None:
            lines.append(self._leaf_desc())
        else:
            lines.append(self.label)

        for i, child in enumerate(self.children):
            child._str_aux(lines, prefix='', is_last=(i == len(self.children) - 1))
        return '\n'.join(lines)

    def _str_aux(self, lines, prefix, is_last):
        connector = '└── ' if is_last else '├── '
        extension = '    ' if is_last else '│   '

        if self.token is not None:
            desc = self._leaf_desc()
        elif self.production is not None:
            desc = f"{self.label}  [{self.production.id}]"
        else:
            desc = self.label

        lines.append(prefix + connector + desc)
        for i, child in enumerate(self.children):
            child._str_aux(lines, prefix + extension, is_last=(i == len(self.children) - 1))

    def display(self):
        print("── Derivation Tree ─────────────────────────────────")
        print(str(self))
        print()

    def display_yield(self):
        forms = [f"'{t.valor}'" for t in self.yield_tokens()]
        print(f"Yield: {' '.join(forms)}\n")

    def _collect_productions(self):
        result = []
        if self.production is not None:
            result.append(self.production)
        for child in self.children:
            result.extend(child._collect_productions())
        return result

    def display_productions_used(self):
        """Prints productions in pre-order = left-most derivation sequence."""
        print("── Productions used ─────────────────────────────────")
        for prod in self._collect_productions():
            print(f"  {prod}")
        print()
