def es_numero_natural(self, lexema):
    # Verifica si el lexema es un número natural
    if lexema.startswith("#"):
        numero = lexema[1:]
        # Verifica si todos los caracteres del número son dígitos
        if self.son_digitos(numero):
            return True
    return False

def son_digitos(self, cadena):
    # Verifica si todos los caracteres de la cadena son dígitos
    for caracter in cadena:
        if caracter not in "0123456789":
            return False
    return True