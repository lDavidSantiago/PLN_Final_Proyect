# semantic.py
# Semantic analysis module.

MAP_ACTIONS = {
    'crear': 'mkdir',
    'mover': 'mv',
    'eliminar': 'rm',
    'copiar': 'cp',
    'renombrar': 'mv',
    'listar': 'ls',
}


class SemanticError(Exception):
    """Raised when the parse tree does not match the expected semantic structure."""


class Semantics:
    """
    Extracts a semantic representation from the parse tree.

    A simple command returns a dict.
    A compound command returns a list of two dicts.
    """

    def extract(self, tree):
        if tree is None or not tree.children:
            raise SemanticError("The parse tree is empty.")

        child = tree.children[0]

        if child.label == 'CMD':
            return self._extract_cmd(child)

        if child.label == 'CMD_COMP':
            return self._extract_cmd_comp(child)

        raise SemanticError(f"Unexpected node under S: '{child.label}'")

    def _extract_cmd_comp(self, node):
        if len(node.children) != 3:
            raise SemanticError("CMD_COMP must contain CMD CONNECTOR CMD.")

        cmd1 = self._extract_cmd(node.children[0])
        cmd2 = self._extract_cmd(node.children[2])
        return [cmd1, cmd2]

    def _extract_cmd(self, node):
        if len(node.children) < 2:
            raise SemanticError("CMD must contain at least VERBS and OBJ.")

        verb_norm = node.children[0].token.valor_norm
        object_info = self._extract_obj(node.children[1])

        destination = None
        if len(node.children) == 3:
            destination = self._extract_dest(node.children[2])

        return {
            'action': MAP_ACTIONS.get(verb_norm, verb_norm),
            'verb': verb_norm,
            'object_type': object_info['object_type'],
            'name': object_info['name'],
            'extension': object_info['extension'],
            'destination': destination,
        }

    def _extract_obj(self, node):
        production_id = node.production.id

        if len(node.children) < 2:
            raise SemanticError("OBJ must contain DET and TYPE.")

        object_type = node.children[1].token.valor_norm
        name = None
        extension = None

        if production_id == 'P6':
            pass
        elif production_id == 'P7':
            extension = node.children[2].token.valor
        elif production_id == 'P8':
            name = node.children[2].token.valor
        elif production_id == 'P9':
            name = node.children[3].token.valor
        elif production_id == 'P10':
            extension = node.children[2].token.valor
            name = node.children[4].token.valor
        else:
            raise SemanticError(f"Unexpected OBJ production: '{production_id}'")

        return {
            'object_type': object_type,
            'name': name,
            'extension': extension,
        }

    def _extract_dest(self, node):
        production_id = node.production.id

        if production_id in ('P11', 'P12'):
            return node.children[1].token.valor

        if production_id == 'P13':
            return node.children[0].token.valor

        raise SemanticError(f"Unexpected DEST production: '{production_id}'")

    def display(self, semantics):
        print("-- Semantic representation --------------------------")
        if isinstance(semantics, list):
            for index, command in enumerate(semantics, 1):
                print(f"  Subcommand {index}:")
                self._display_dict(command, indent='    ')
        else:
            self._display_dict(semantics, indent='  ')
        print()

    def _display_dict(self, data, indent='  '):
        for key, value in data.items():
            if value is not None:
                print(f"{indent}{key:<12}: {value}")


if __name__ == '__main__':
    from lexer import Lexer
    from parser import Parser

    lexer = Lexer()
    parser = Parser()
    semantics = Semantics()

    cases = [
        "crea una carpeta llamada proyectos",
        "mueve los archivos pdf a respaldo",
        "elimina la carpeta vieja",
        "copia el archivo txt a respaldo",
        "renombra la carpeta vieja llamada nueva",
        "lista los archivos",
        "crea una carpeta llamada datos y mueve los archivos csv a respaldo",
    ]

    for text in cases:
        print("=" * 70)
        print(f"Input: {text}")
        tokens = lexer.tokenizar(text)
        tree = parser.parse(tokens)
        tree.display()
        rep = semantics.extract(tree)
        semantics.display(rep)