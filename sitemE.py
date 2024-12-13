import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Automata import *
from Token import *
from TokenType import *

def analisis_lexico(proposicion):
    # Cambiar frase a minusculas y separar por espacios
    tokens = proposicion.lower().split(' ')

    # Tokenizar palabras
    listaTokens = []
    for token in tokens:
        if token == 'y':
            listaTokens.append(Token(TokenType.Y, token))
        elif token == 'o':
            listaTokens.append(Token(TokenType.O, token))
        elif token == 'si':
            listaTokens.append(Token(TokenType.SI, token))
        elif token == 'entonces':
            listaTokens.append(Token(TokenType.ENTONCES, token))
        elif token == 'no':
            listaTokens.append(Token(TokenType.NOT, token))
        else:
            listaTokens.append(Token(TokenType.PALABRA, token))
    listaTokens.append(Token(TokenType.EOL, ''))
    return listaTokens

def print_ast(node, level=0):
    indent = "  " * level
    if isinstance(node, PropNode):
        return f"{indent}PropNode: {node}\n"
    elif isinstance(node, NegNode):
        return f"{indent}NegNode\n" + print_ast(node.child, level + 1)
    elif isinstance(node, OperatorNode):
        return (
            f"{indent}CondNode: {node.operator}\n"
            + print_ast(node.left, level + 1)
            + print_ast(node.right, level + 1)
        )
    return ""

def dibujar_arbol(grafo, titulo):
    pos = nx.spring_layout(grafo)
    plt.figure(figsize=(12, 8))
    nx.draw(grafo, pos, with_labels=True, node_color="lightblue", font_size=10, node_size=3000)
    plt.title(titulo)
    plt.show()

def generar_arbol_ast(node, grafo=None, current_id=1):
    if grafo is None:
        grafo = nx.DiGraph()

    if isinstance(node, PropNode):
        grafo.add_node(current_id, label=f"PropNode ({node})")
        return grafo, current_id

    if isinstance(node, NegNode):
        grafo.add_node(current_id, label="NegNode")
        grafo, child_id = generar_arbol_ast(node.child, grafo, current_id + 1)
        grafo.add_edge(current_id, child_id)
        return grafo, current_id

    if isinstance(node, OperatorNode):
        grafo.add_node(current_id, label=f"CondNode ({node.operator})")
        grafo, left_id = generar_arbol_ast(node.left, grafo, current_id + 1)
        grafo.add_edge(current_id, left_id)
        grafo, right_id = generar_arbol_ast(node.right, grafo, left_id + 1)
        grafo.add_edge(current_id, right_id)
        return grafo, current_id

    return grafo, current_id

def analizar_proposiciones():
    proposiciones = entrada.get("1.0", tk.END).strip().split("\n")  # Separar frases por nueva línea
    if not proposiciones or len(proposiciones) == 0:
        messagebox.showerror("Error", "Por favor ingresa al menos una proposición.")
        return

    salida_lexico.delete("1.0", tk.END)
    salida_sintactico.delete("1.0", tk.END)
    fig.clear()

    for i, proposicion in enumerate(proposiciones[:10]):  # Limitar a 10 frases
        if not proposicion.strip():
            continue

        salida_lexico.insert(tk.END, f"========== Proposición {i + 1} ==========\n")
        salida_lexico.insert(tk.END, f"Frase: {proposicion}\n\n")
        tokens = analisis_lexico(proposicion)

        # Mostrar análisis léxico
        salida_lexico.insert(tk.END, "Tipo\tValor\n")
        for token in tokens:
            salida_lexico.insert(tk.END, f"{token.tipo}\t{token.valor}\n")
        salida_lexico.insert(tk.END, "\n")

        # Realizar análisis sintáctico y semántico
        automata = Automata()
        resultado = automata.evaluar(tokens)

        salida_sintactico.insert(tk.END, f"========== Proposición {i + 1} ==========\n")
        if resultado:
            salida_sintactico.insert(tk.END, f"AST generado:\n")
            ast = print_ast(resultado)
            salida_sintactico.insert(tk.END, ast + "\n")

            # Generar y mostrar árbol AST
            grafo_ast, _ = generar_arbol_ast(resultado)
            nx.draw(grafo_ast, with_labels=True, labels=nx.get_node_attributes(grafo_ast, 'label'))
            canvas.draw()
        else:
            salida_sintactico.insert(tk.END, f"La proposición es incorrecta.\n\n")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Analizador de Proposiciones")

# Crear pestañas
tabs = ttk.Notebook(ventana)
tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tabs.add(tab1, text='Análisis')
tabs.add(tab2, text='Árbol AST')
tabs.pack(expand=1, fill="both")

# Entrada de proposiciones
frame_entrada = tk.Frame(tab1)
frame_entrada.pack(pady=10)

etiqueta = tk.Label(frame_entrada, text="Ingrese proposiciones (una por línea, máx. 10):")
etiqueta.pack()

entrada = tk.Text(frame_entrada, height=10, width=60)
entrada.pack(pady=5)

boton_analizar = tk.Button(frame_entrada, text="Analizar", command=analizar_proposiciones)
boton_analizar.pack(pady=5)

# Salida de análisis léxico
frame_lexico = tk.Frame(tab1)
frame_lexico.pack(pady=10)

etiqueta_lexico = tk.Label(frame_lexico, text="Análisis Léxico:")
etiqueta_lexico.pack()

salida_lexico = tk.Text(frame_lexico, height=10, width=80)
salida_lexico.pack()

# Salida de análisis sintáctico y semántico
frame_sintactico = tk.Frame(tab1)
frame_sintactico.pack(pady=10)

etiqueta_sintactico = tk.Label(frame_sintactico, text="Análisis Sintáctico y Semántico:")
etiqueta_sintactico.pack()

salida_sintactico = tk.Text(frame_sintactico, height=15, width=80)
salida_sintactico.pack()

# Pestaña de Árbol AST
frame_arbol = tk.Frame(tab2)
frame_arbol.pack(pady=10)

fig = plt.figure(figsize=(12, 8))
canvas = FigureCanvasTkAgg(fig, master=frame_arbol)
canvas.get_tk_widget().pack()

# Iniciar bucle de la aplicación
def main():
    ventana.mainloop()

if __name__ == "__main__":
    main()

# Modificación para soportar múltiples operadores
class Automata:
    def __init__(self):
        self.estadoActual = AutomataEstado.INICIO
        self.ast = None
        self.ultimo_nodo = None

    def transition(self, input_token):
        # Transición original, adaptada para manejar múltiples operadores
        if input_token.tipo in [TokenType.Y, TokenType.O]:
            operator = OperatorType.AND if input_token.tipo == TokenType.Y else OperatorType.OR

            if isinstance(self.ast, OperatorNode) and self.ast.operator == operator:
                # Encadenar operadores del mismo tipo
                self.ast.right = OperatorNode(self.ast.right, operator, None)
                self.ultimo_nodo = self.ast.right
            else:
                # Crear nuevo operador con el árbol actual a la izquierda
                self.ast = OperatorNode(self.ast, operator, None)
                self.ultimo_nodo = self.ast

        elif input_token.tipo == TokenType.PALABRA:
            prop = PropNode(input_token)
            if self.ultimo_nodo and isinstance(self.ultimo_nodo, OperatorNode) and self.ultimo_nodo.right is None:
                self.ultimo_nodo.right = prop
            elif self.ast is None:
                self.ast = prop
            self.ultimo_nodo = prop

    def evaluar(self, listaTokens):
        for token in listaTokens:
            self.transition(token)
        return self.ast
