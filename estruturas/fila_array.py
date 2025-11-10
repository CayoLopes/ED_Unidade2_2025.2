# estruturas/fila_array.py
class FilaArray:
    def __init__(self):
        self.dados = []

    def adicionar(self, item):
        self.dados.append(item)

    def remover(self):
        if not self.vazia():
            return self.dados.pop(0)
        return None

    def aumentar_tamanho(self):
        self.dados.extend([None] * len(self.dados))

    def diminuir_tamanho(self):
        metade = len(self.dados) // 2
        self.dados = self.dados[:metade]

    def vazia(self):
        return len(self.dados) == 0
