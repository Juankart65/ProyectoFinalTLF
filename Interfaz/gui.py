import re
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Define las expresiones regulares para los tokens
TOKEN_REGEX = {
    'NUM_NATURAL': r'^\d+$',
    'NUM_REAL': r'^#-?\d+(\.\d+)?',
    'IDENTIFICADOR': r'^[a-zA-Z_]\w{0,9}$',
    'RESERVADA': r'^(if|else|while|return|int|float)$',  # Ajusta según las palabras reservadas que elijas
    'OP_ARITMETICO': r'^[+\-*/%]$',
    'OP_COMPARACION': r'^(==|!=|<|<=|>|>=)$',
    'OP_LOGICO': r'^(and|or|not)$',
    'OP_ASIGNACION': r'^=$',
    'OP_INC_DEC': r'^(--|\+\+)$',
    'PARENTESIS': r'^[()]$',
    'LLAVE': r'^[{}]$',
    'TERMINAL': r'^;$',
    'SEPARADOR': r'^,$',
    'HEX': r'^[0-9A-Fa-f]+$',
    'CADENA': r'^".*"$',
    'COMENTARIO_LINEA': r'^//.*$',
    'COMENTARIO_BLOQUE': r'^/\*.*\*/$'
}

class Token:
    def __init__(self, tipo, lexema, posicion):
        self.tipo = tipo
        self.lexema = lexema
        self.posicion = posicion

    def __str__(self):
        return f"{self.tipo}: '{self.lexema}' en {self.posicion}"

class AnalizadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []
        self.errores = []

    def analizar(self):
        self.tokens.clear()
        self.errores.clear()
        lineas = self.codigo.split('\n')
        for numero_linea, linea in enumerate(lineas, start=1):
            posicion = 0
            while posicion < len(linea):
                token, length = self._obtener_siguiente_token(linea[posicion:])
                if token:
                    token.posicion = (numero_linea, posicion)
                    self.tokens.append(token)
                    posicion += length
                else:
                    self.errores.append(f"Error léxico en línea {numero_linea} posición {posicion}")
                    posicion += 1

    def _obtener_siguiente_token(self, texto):
        for tipo, regex in TOKEN_REGEX.items():
            match = re.match(regex, texto)
            if match:
                lexema = match.group(0)
                return Token(tipo, lexema, None), len(lexema)
        return None, 0

class AnalizadorLexicoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
        self.text_area.grid(row=0, column=0, padx=10, pady=10)

        self.analyze_button = tk.Button(root, text="Analizar", command=self.analizar_codigo)
        self.analyze_button.grid(row=1, column=0, pady=10)

        self.result_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, state='disabled')
        self.result_area.grid(row=2, column=0, padx=10, pady=10)

    def analizar_codigo(self):
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

# Ejecución de la interfaz gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorLexicoGUI(root)
    root.mainloop()
