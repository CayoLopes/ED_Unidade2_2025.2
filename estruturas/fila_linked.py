# estruturas/fila_linked.py
class Node:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class FilaLinked:
    def __init__(self):
        self.frente = None
        self.tras = None
        self.tamanho = 0

    def adicionar(self, item):
        novo = Node(item)
        if self.tras:
            self.tras.proximo = novo
        self.tras = novo
        if not self.frente:
            self.frente = novo
        self.tamanho += 1

    def remover(self):
        if not self.frente:
            return None
        valor = self.frente.valor
        self.frente = self.frente.proximo
        if not self.frente:
            self.tras = None
        self.tamanho -= 1
        return valor

    def aumentar_tamanho(self):
        for _ in range(self.tamanho):
            self.adicionar(None)

    def diminuir_tamanho(self):
        for _ in range(self.tamanho // 2):
            self.remover()
