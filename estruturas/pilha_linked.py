# estruturas/pilha_linked.py
class Node:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class PilhaLinked:
    def __init__(self):
        self.topo = None
        self.tamanho = 0

    def adicionar(self, item):
        novo = Node(item)
        novo.proximo = self.topo
        self.topo = novo
        self.tamanho += 1

    def remover(self):
        if self.topo:
            valor = self.topo.valor
            self.topo = self.topo.proximo
            self.tamanho -= 1
            return valor
        return None

    def aumentar_tamanho(self):
        for _ in range(self.tamanho):
            self.adicionar(None)

    def diminuir_tamanho(self):
        for _ in range(self.tamanho // 2):
            self.remover()
