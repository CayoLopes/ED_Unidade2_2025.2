# estruturas/lista_array.py
class ListaArray:
    def __init__(self):
        self.dados = []

    def adicionar(self, item):
        self.dados.append(item)

    def remover(self, item=None):
        if not self.vazia():
            if item is not None and item in self.dados:
                self.dados.remove(item)
            else:
                self.dados.pop()

    def aumentar_tamanho(self):
        self.dados.extend([None] * len(self.dados))

    def diminuir_tamanho(self):
        metade = len(self.dados) // 2
        self.dados = self.dados[:metade]

    def vazia(self):
        return len(self.dados) == 0
