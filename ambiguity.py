# Ambiguity Detection 

"""
    Tipes of ambiguity we can detect:
    Syntactic ambiguity: This happend when a sentence can be parsed in more than one way. For example, 
    S -> elimina los archivos de documentos
    AMbiguity 1: documentos DENTRO de la carpeta 'documentos'
    Ambiguity 2: documentos COMO el tipo de archivos a eliminar (.pdf,.doc)
"""
from semantic import MAP_ACTIONS

class Interpretation:
    
    def __init__(self,number,description,semantic):
        self.number = number
        self.description = description
        self.semantic = semantic
    
    def __repr__(self):
        return f"Interpretation {self.number}: {self.description}"
    

class AmbiguityResponse:
    
    def __init__(self,is_ambiguous,interpretations = None, message = ''):
        
        self.is_ambiguous = is_ambiguous
        self.interpretations = interpretations or []
        self.message = message
        
class AmbiguityDetector:
    
    def analize (self,tokens):
    # We get the tokens types to detect ambiguity by patterns of token types
        token_types = [t.tipo for t in tokens]
    
    # --------------- Verification 1 -----------------
    #   # Pattern: VERB + DET + TYPE + PREP + NAME
    #   # Example: "crea una carpeta llamada proyectos"
    #   # When prep is "de"
    
        response = self._detect_specific_pattern(tokens,token_types)
        if response.is_ambiguous:
            return response
        
    # --------------- Verification 2 -----------------
    #   implicit destination ambiguity
        response = self._detect_implicit_destination(tokens,token_types)
        if response.is_ambiguous:
            return response

        return AmbiguityResponse(is_ambiguous=False)

    def _detect_specific_pattern(self,tokens,token_types):
        
        patter = ['VERBS','DET','TYPE','PREP','NAMING']
        
        if token_types != patter:
            return AmbiguityResponse(is_ambiguous=False)
        
        # Verify if the PREP is "de"
        prep_token = tokens[3]
        if prep_token.valor.lower() != 'de':
            return AmbiguityResponse(is_ambiguous=False)
        
        verb = tokens[0].valor_norm
        token_type = tokens[2].valor_norm
        name = tokens[4].valor
        
        action = MAP_ACTIONS.get(verb, verb)
        
        sem1 ={
            'action': action,
            'verb': verb,
            'object_type': token_type,
            'name': None,
            'extension': None,
            'destination': name, 
        }
        interpretation1 = Interpretation(1,f"{name} is the destination of the action",sem1)
        
        sem2 ={
            'action': action,
            'verb': verb,
            'object_type': token_type,
            'name': name,
            'extension': None,
            'destination': None, 
        }
        interpretation2 = Interpretation(2,f"{name} is the name of the object",sem2)
        
        return AmbiguityResponse(is_ambiguous=True,
                                 interpretations=[interpretation1,interpretation2],
                                message           = (
                f"====================AMBIGUITY DETECTED====================\n"
                f"  The phrase 'de {name}' can be attached in two ways:\n"
                f"    a) To the CMD  => indicates LOCATION (source folder)\n"
                f"    b) To the OBJ  => indicates TYPE or NAME of the object"
            ),
        )
    def _detect_implicit_destination(self,tokens,token_types):
        """
         tHis ones detect the ambiguity when destination is not explicitly stated
        
        Patter -> VERB  + DET + TYPE + NAME
        
        ej: "mueve el archivo pdf informe
        Ambiguitye -> The name at the end could be:
        a) The name of the object could be "informe.pdf"
        b ) The implicit destination could be move the .pdf files to -> "informe" folder
        
        as we dont see any clear preposition like "a" or "hacia" to destinate the destination,
        we can assume that the last token could be either the name of the object or the destination.
        
        """
        
        patter = ['VERBS', 'DET', 'TYPE', 'EXT', 'NAMING']
        if token_types != patter:
            return AmbiguityResponse(is_ambiguous=False)
        
        
        verb = tokens[0].valor_norm
        token_type = tokens[2].valor_norm
        extension = tokens[3].valor
        name = tokens[4].valor
        
        action = MAP_ACTIONS.get(verb, verb)
        
        # Only is ambiguous if verb is "mover" or "copiar" 
        # because they are the ones that can have a destination
        if verb not in ['mover','copiar']:
            return AmbiguityResponse(is_ambiguous=False)
        
        sem1 = {
            'action'     : action,
            'verb'      : verb,
            'object_type': token_type,
            'name'     : None,
            'extension'  : extension,
            'destination'    : name,
        }
        interpretation1 = Interpretation(
            number=1,
            description=(f"All the objects of type {token_type} with extension {extension} will be moved to the folder '{name}'\n"
                         f" This equals to {action} *.{extension} a {name}"),
            semantic=sem1
        )
        
        sem2 = {
            'action'     : action,
            'verb'      : verb,
            'object_type': token_type,
            'name'     : name,
            'extension'  : extension,
            'destination'    : None,
        }
        interpretation2 = Interpretation(
            number=2,
            description=(f"The object '{name}' will be moved to the folder '{name}'\n"
                         f" This equals to {action} {name} a {name}"),
            semantic=sem2
        )

        return AmbiguityResponse(is_ambiguous=True, interpretations=[interpretation1, interpretation2])
    
    
class AmbiguityResolver:
    
    def __init__(self):
        self.detector = AmbiguityDetector()
    
    def verify_and_resolve(self,tokens):
        response = self.detector.analize(tokens)
        if not response.is_ambiguous:
            return None
        print("-- Ambiguedad detectada ----------------------------")
        print(response.message)
        print("-- Interpretaciones posibles -----------------------")
        for interpretation in response.interpretations:
            print(interpretation)
        print("  El sistema NO ejecutara la accion hasta resolver la ambiguedad.")



        while True:
            try:
                choice = int(input("Select the correct interpretation (enter the number): "))
                selected = next((i for i in response.interpretations if i.number == choice), None)
                if selected is not None:
                    return selected.semantic
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    def display(self,tokens):
        result =self.detector.analize(tokens)
        if not result.is_ambiguous:
            print("No ambiguity detected.")
            return
        print("-- Ambiguedad detectada ----------------------------")
        print(result.message)
        print("-- Interpretaciones posibles -----------------------")
        for interpretation in result.interpretations:
            print(interpretation)
        print("  El sistema NO ejecutara la accion hasta resolver la ambiguedad.")
        
if __name__ == "__main__":
    from lexer import Lexer
    lexer    = Lexer()
    resolver = AmbiguityResolver()
    
    ambiguous_cases = [
        ("SP ambiguo con 'de'",       "elimina los archivos de documentos"),
        ("SP ambiguo con 'de' (mv)",  "mueve los archivos de proyectos"),
        ("Destino implicito",         "mueve los archivos pdf documentos"),
        ("Destino implicito (cp)",    "copia los archivos txt respaldo"),
    ]
    
    not_ambiguous_cases = [
        ("Sin ambiguedad",            "crea una carpeta llamada proyectos"),
        ("Sin ambiguedad",            "mueve los archivos pdf a proyectos"),
        ("Sin ambiguedad",            "elimina los archivos"),
    ]
    
    print("=" * 60)
    print("CASOS AMBIGUOS (solo visualizacion, sin input interactivo)")
    print("=" * 60)
    
    for description, text in ambiguous_cases:
        print(f"\nCaso: {description}")
        print(f"Input: {text}")
        tokens = lexer.tokenizar(text)
        lexer.display_tokens(tokens)
        resolver.display(tokens)
    
    print("=" * 60)
    print("CASOS NO AMBIGUOS")
    print("=" * 60)
    for description, text in not_ambiguous_cases:
        print(f"\nCaso: {description}")
        print(f"Input: {text}")
        tokens = lexer.tokenizar(text)
        lexer.display_tokens(tokens)
        resolver.display(tokens)