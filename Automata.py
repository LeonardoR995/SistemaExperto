from TokenType import TokenType
from Token import Token
from AutomataEstado import AutomataEstado
from ASTNodes import *

from TokenType import TokenType
from Token import Token
from AutomataEstado import AutomataEstado
from ASTNodes import *

class Automata:
    def __init__(self):
        self.operadores = []  # Pila de operadores
        self.operandos = []  # Pila de operandos


    def aplicar_operador(self):
        if len(self.operadores) > 0 and len(self.operandos) >= 2:
            operador = self.operadores.pop()
            derecho = self.operandos.pop()
            izquierdo = self.operandos.pop()
            self.operandos.append(OperatorNode(izquierdo, operador, derecho))

    def prioridad(self, operador):
        if operador == OperatorType.AND:
            return 2
        elif operador == OperatorType.OR:
            return 1
        return 0

    def transition(self, input_token):
        if input_token.tipo in [TokenType.Y, TokenType.O]:
            operador_actual = OperatorType.AND if input_token.tipo == TokenType.Y else OperatorType.OR
            while (
                len(self.operadores) > 0 and
                self.prioridad(self.operadores[-1]) >= self.prioridad(operador_actual)
            ):
                self.aplicar_operador()
            self.operadores.append(operador_actual)

        elif input_token.tipo == TokenType.PALABRA:
            self.operandos.append(PropNode(input_token))

    def evaluar(self, listaTokens):
        for token in listaTokens:
            if token.tipo != TokenType.EOL:
                self.transition(token)

        while len(self.operadores) > 0:
            self.aplicar_operador()

        return self.operandos[0] if len(self.operandos) == 1 else None

        for token in listaTokens:
            self.transition(token)
            if self.estadoActual == AutomataEstado.ERROR:
                return None
        return self.ast if self.is_accepting() else None
