import re
class AFDNumeroReal:
    def __init__(self):
        self.estado_actual = 0
        self.lexema = ""

    def es_digito_real(self, caracter):
        return bool(re.match(r'^#-?\d+(\.\d+)?', caracter))

    def transicion(self, caracter):
        self.lexema += caracter
        if self.estado_actual == 0:
            if caracter in '+-':
                self.estado_actual = 1
            elif '0' <= caracter <= '9':
                self.estado_actual = 2
            else:
                self.estado_actual = -1
        elif self.estado_actual == 1:
            if '0' <= caracter <= '9':
                self.estado_actual = 2
            else:
                self.estado_actual = -1
        elif self.estado_actual == 2:
            if '0' <= caracter <= '9':
                self.estado_actual = 2
            elif caracter == '.':
                self.estado_actual = 3
            else:
                self.estado_actual = -1
        elif self.estado_actual == 3:
            if '0' <= caracter <= '9':
                self.estado_actual = 4
            else:
                self.estado_actual = -1
        elif self.estado_actual == 4:
            if '0' <= caracter <= '9':
                self.estado_actual = 4
            else:
                self.estado_actual = -1

        print(self.estado_actual)

    def es_estado_aceptacion(self):
        return self.estado_actual == 2 or self.estado_actual == 4

    def reiniciar(self):
        self.estado_actual = 0
        self.lexema = ""
