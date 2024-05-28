class AFDNumeroEntero:
    def __init__(self):
        self.estado_actual = 0

    def es_digito(self, caracter):
        return '0' <= caracter <= '9'

    def transicion(self, caracter):
        if self.estado_actual == 0:
            if caracter == '-':
                self.estado_actual = 1
            elif self.es_digito(caracter):
                self.estado_actual = 2
            else:
                self.estado_actual = -1
        elif self.estado_actual == 1:
            if self.es_digito(caracter):
                self.estado_actual = 2
            else:
                self.estado_actual = -1
        elif self.estado_actual == 2:
            if self.es_digito(caracter):
                self.estado_actual = 2
            elif caracter == '.':
                self.estado_actual = 3
            else:
                self.estado_actual = -1
        elif self.estado_actual == 3:
            if self.es_digito(caracter):
                self.estado_actual = 4
            else:
                self.estado_actual = -1
        elif self.estado_actual == 4:
            if self.es_digito(caracter):
                self.estado_actual = 4
            elif caracter == '.':
                self.estado_actual = 3
            else:
                self.estado_actual = -1

    def es_estado_aceptacion(self):
        return self.estado_actual == 2 or self.estado_actual == 4

    def reiniciar(self):
        self.estado_actual = 0
