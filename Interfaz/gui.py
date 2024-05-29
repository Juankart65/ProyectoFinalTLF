import tkinter as tk
from tkinter import scrolledtext, filedialog
import docx

class Token:
    def __init__(self, tipo, lexema, posicion):
        self.tipo = tipo
        self.lexema = lexema
        self.posicion = posicion

    def __str__(self):
        return f"{self.tipo}: '{self.lexema}' en {self.posicion}"

class AnalizadorLexico:
    OP_ARITMETICOS = {'Sum', 'Res', 'Mul', 'Div', 'Mod', 'Pot', 'Root', 'Fact', 'Ln', 'Log'}
    OP_COMPARACION = {'eq', 'Noeq', '++', '--eq', '--', '++eq'}
    OP_LOGICOS = {'Clip', 'Sep', 'Nah'}
    OP_ASIGNACION = {'Ig', 'SumIg', 'ResIg', 'MulIg', 'DivIg'}
    ESPACIOS = {' ', '\t', '\n'}
    TERMINALES = {';', ','}
    SIMBOLOS_ABRIR = {'¿', '<', '|'}
    SIMBOLOS_CERRAR = {'?', '>', '|'}
    CICLOS = {'hagale', 'hagale-mientras', 'primero-hagale'}
    DESICION = {'depende-si', 'y-si-no'}
    CLASES = {'chuspa', 'popeta'}
    ID_VAR = {'cosa'}
    ID_METODO = {'vainas'}
    ID_ENTEROS = {'palo'}
    ID_REALES = {'media', 'litro'}
    ID_STRING = {'parla'}
    ID_CARACTER = {'trama'}
    ID_BOOLEANS = {'szs', 'nns'}
    ID_EXCEPCION = {'Murph'}

    
    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []
        self.errores = []

    def analizar(self):
        self.tokens.clear()
        self.errores.clear()
        posicion = 0
        linea_actual = 1
        
        while posicion < len(self.codigo):
            if self.codigo[posicion] in self.ESPACIOS:
                if self.codigo[posicion] == '\n':
                    linea_actual += 1
                posicion += 1
                continue
            
            token, length = self._obtener_siguiente_token(self.codigo[posicion:], linea_actual, posicion)
            if token:
                self.tokens.append(token)
                posicion += length
            else:
                self.errores.append(f"Error léxico en línea {linea_actual} posición {posicion}")
                posicion += 1

    def _obtener_siguiente_token(self, texto, linea_actual, posicion_actual):
        # Ordenar operadores de comparación por longitud descendente para que '==' se detecte antes que '='
        operadores = sorted(self.OP_COMPARACION, key=len, reverse=True)

        for op in operadores:
            if texto.startswith(op):
                return Token("OP_COMPARACION", op, (linea_actual, posicion_actual)), len(op)
        
        for op in self.OP_ARITMETICOS:
            if texto.startswith(op):
                return Token("OP_ARITMETICO", op, (linea_actual, posicion_actual)), len(op)
        
        for op in self.OP_LOGICOS:
            if texto.startswith(op):
                return Token("OP_LOGICO", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.CICLOS:
            if texto.startswith(op):
                return Token("CICLOS", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.SIMBOLOS_ABRIR:
            if texto.startswith(op):
                return Token("SIMBOLOS_ABRIR", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.SIMBOLOS_CERRAR:
            if texto.startswith(op):
                return Token("SIMBOLOS_CERRAR", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.DESICION:
            if texto.startswith(op):
                return Token("DESICION", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.CLASES:
            if texto.startswith(op):
                return Token("CLASES", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.ID_VAR:
            if texto.startswith(op):
                return Token("ID_VAR", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.ID_STRING:
            if texto.startswith(op):
                return Token("ID_STRING", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.ID_BOOLEANS:
            if texto.startswith(op):
                return Token("ID_BOOLEANS", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.ID_CARACTER:
            if texto.startswith(op):
                return Token("ID_CARACTER", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.ID_ENTEROS:
            if texto.startswith(op):
                return Token("ID_ENTEROS", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.ID_REALES:
            if texto.startswith(op):
                return Token("ID_REALES", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.ID_EXCEPCION:
            if texto.startswith(op):
                return Token("ID_EXCEPCION", op, (linea_actual, posicion_actual)), len(op)
            
        for op in self.ID_METODO:
            if texto.startswith(op):
                return Token("ID_METODO", op, (linea_actual, posicion_actual)), len(op)

        # Identificar números naturales y reales
        if texto.startswith('#'):
            return self._match_numero(texto, linea_actual, posicion_actual)

        # Identificar otros caracteres
        if texto[0] in self.TERMINALES:
            return Token("TERMINAL", texto[0], (linea_actual, posicion_actual)), 1

        # Identificar identificadores y palabras clave
        if texto[0].isalpha() or texto[0] == '_':
            return self._match_identificador(texto, linea_actual, posicion_actual)

        # Si no se reconoce el token
        return None, 0

    def _match_numero(self, texto, linea_actual, posicion_actual):
        posicion = 1
        if len(texto) > 1 and texto[posicion] == '-':
            posicion += 1
        while posicion < len(texto) and texto[posicion].isdigit():
            posicion += 1
        if posicion < len(texto) and texto[posicion] == '.':
            posicion += 1
            while posicion < len(texto) and texto[posicion].isdigit():
                posicion += 1
            return Token("NUM_REAL", texto[:posicion], (linea_actual, posicion_actual)), posicion
        return Token("NUM_NATURAL", texto[:posicion], (linea_actual, posicion_actual)), posicion

    def _match_identificador(self, texto, linea_actual, posicion_actual):
        posicion = 1
        while posicion < len(texto) and (texto[posicion].isalnum() or texto[posicion] == '_'):
            posicion += 1
        return Token("IDENTIFICADOR", texto[:posicion], (linea_actual, posicion_actual)), posicion

class AnalizadorLexicoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
        self.text_area.grid(row=0, column=0, padx=10, pady=10)

        self.load_button = tk.Button(root, text="Cargar Documento", command=self.cargar_documento)
        self.load_button.grid(row=1, column=0, pady=10)

        self.analyze_button = tk.Button(root, text="Analizar", command=self.analizar_codigo)
        self.analyze_button.grid(row=1, column=1, pady=10)

        self.result_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, state='disabled')
        self.result_area.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    def cargar_documento(self):
        filepath = filedialog.askopenfilename(filetypes=[("Documentos de Word", "*.docx"), ("Todos los archivos", "*.*")])
        if filepath:
            doc = docx.Document(filepath)
            texto = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, texto)

    def analizar_codigo(self):
        if self.text_area.get("1.0", tk.END).strip():
            codigo = self.text_area.get("1.0", tk.END).strip()
            analizador = AnalizadorLexico(codigo)
            analizador.analizar()

            self.result_area.config(state='normal')
            self.result_area.delete("1.0", tk.END)

            if analizador.errores:
                for error in analizador.errores:
                    self.result_area.insert(tk.END, error + '\n')
            else:
                for token in analizador.tokens:
                    self.result_area.insert(tk.END, str(token) + '\n')

            self.result_area.config(state='disabled')
        else:
            tk.messagebox.showwarning("Advertencia", "Por favor, ingresa o carga un código para analizar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorLexicoGUI(root)
    root.mainloop()