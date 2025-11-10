# estruturas/lista_linked.py
class Node:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class ListaLinked:
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0

    def adicionar(self, item):
        novo = Node(item)
        if not self.cabeca:
            self.cabeca = novo
        else:
            atual = self.cabeca
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo
        self.tamanho += 1

    def remover(self, item=None):
        if not self.cabeca:
            return
        if item is None:
            # remove o último
            if self.cabeca.proximo is None:
                self.cabeca = None
            else:
                atual = self.cabeca
                while atual.proximo and atual.proximo.proximo:
                    atual = atual.proximo
                atual.proximo = None
        else:
            # remove item específico
            atual = self.cabeca
            anterior = None
            while atual:
                if atual.valor == item:
                    if anterior:
                        anterior.proximo = atual.proximo
                    else:
                        self.cabeca = atual.proximo
                    break
                anterior = atual
                atual = atual.proximo
        self.tamanho -= 1 if self.tamanho > 0 else 0

    def aumentar_tamanho(self):
        for _ in range(self.tamanho):
            self.adicionar(None)

    def diminuir_tamanho(self):
        for _ in range(self.tamanho // 2):
            self.remover()
