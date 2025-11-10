# medir_tempos.py
import time
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

# Importações das estruturas
from estruturas.pilha_array import PilhaArray
from estruturas.pilha_linked import PilhaLinked
from estruturas.fila_array import FilaArray
from estruturas.fila_linked import FilaLinked
from estruturas.lista_array import ListaArray
from estruturas.lista_linked import ListaLinked


def medir_tempo(funcao):
    inicio = time.perf_counter()
    funcao()
    return time.perf_counter() - inicio


def testar_estrutura(estrutura_cls, nome, n_max):
    resultados = []
    for n in range(1, n_max + 1):
        estrutura = estrutura_cls()
        tempos = {}

        # Adicionar elementos
        tempos["adicionar"] = medir_tempo(lambda: [estrutura.adicionar(i) for i in range(n)])

        # Remover elementos
        [estrutura.adicionar(i) for i in range(n)]
        tempos["remover"] = medir_tempo(lambda: [estrutura.remover() for _ in range(n)])

        # Aumentar tamanho físico
        [estrutura.adicionar(i) for i in range(n)]
        tempos["aumentar"] = medir_tempo(lambda: estrutura.aumentar_tamanho())

        # Diminuir tamanho físico
        tempos["diminuir"] = medir_tempo(lambda: estrutura.diminuir_tamanho())

        resultados.append([nome, n, tempos["adicionar"], tempos["remover"], tempos["aumentar"], tempos["diminuir"]])
        print(f"[OK] {nome} - N={n}")
    return resultados


def salvar_csv(nome_arquivo, resultados):
    os.makedirs("resultados", exist_ok=True)
    caminho = os.path.join("resultados", nome_arquivo)
    with open(caminho, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["estrutura", "n", "adicionar", "remover", "aumentar", "diminuir"])
        writer.writerows(resultados)
    print(f"✔ Resultados salvos em {caminho}")


def gerar_graficos(nome_csv, titulo):
    os.makedirs("graficos", exist_ok=True)
    df = pd.read_csv(os.path.join("resultados", nome_csv))

    for operacao in ["adicionar", "remover", "aumentar", "diminuir"]:
        plt.figure(figsize=(8, 5))
        for estrutura in df["estrutura"].unique():
            dados = df[df["estrutura"] == estrutura]
            plt.plot(dados["n"], dados[operacao], label=estrutura)
        plt.title(f"{titulo} - Tempo de execução ({operacao})")
        plt.xlabel("Tamanho de N")
        plt.ylabel("Tempo (segundos)")
        plt.legend()
        plt.grid(True)
        nome_img = f"{titulo.lower()}_{operacao}.png".replace(" ", "_")
        plt.savefig(os.path.join("graficos", nome_img))
        plt.close()
    print(f"📈 Gráficos de {titulo} gerados em /graficos")


if __name__ == "__main__":
    n_max = int(input("Digite o valor máximo de N: "))

    # Estruturas e agrupamentos
    grupos = {
        "pilha.csv": [
            ("Pilha (Array)", PilhaArray),
            ("Pilha (LinkedList)", PilhaLinked)
        ],
        "fila.csv": [
            ("Fila (Array)", FilaArray),
            ("Fila (LinkedList)", FilaLinked)
        ],
        "lista.csv": [
            ("Lista (Array)", ListaArray),
            ("Lista (LinkedList)", ListaLinked)
        ],
    }

    for nome_arquivo, estruturas in grupos.items():
        resultados = []
        for nome, classe in estruturas:
            resultados += testar_estrutura(classe, nome, n_max)
        salvar_csv(nome_arquivo, resultados)
        gerar_graficos(nome_arquivo, nome_arquivo.replace(".csv", "").capitalize())
    
    print("\n✅ Testes concluídos com sucesso!")
    print("Arquivos salvos na pasta 'resultados/' e gráficos em 'graficos/'")
