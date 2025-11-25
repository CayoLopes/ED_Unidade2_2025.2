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
    
    for n in range(0, n_max + 1, 50):
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


def gerar_graficos_comparacao(nome_csv, titulo):
    """Gera gráficos comparando Array vs LinkedList (original)"""
    os.makedirs("graficos/comparacao", exist_ok=True)
    df = pd.read_csv(os.path.join("resultados", nome_csv))

    for operacao in ["adicionar", "remover", "aumentar", "diminuir"]:
        plt.figure(figsize=(8, 5))
        for estrutura in df["estrutura"].unique():
            dados = df[df["estrutura"] == estrutura]
            plt.plot(dados["n"], dados[operacao], label=estrutura, marker='o', markersize=3)
        plt.title(f"{titulo} - Comparação Array vs LinkedList ({operacao})")
        plt.xlabel("Tamanho de N")
        plt.ylabel("Tempo (segundos)")
        plt.legend()
        plt.grid(True)
        nome_img = f"comparacao_{titulo.lower()}_{operacao}.png".replace(" ", "_")
        plt.savefig(os.path.join("graficos/comparacao", nome_img))
        plt.close()
    print(f" Gráficos de comparação de {titulo} gerados em /graficos/comparacao")


def gerar_graficos_individual(nome_csv, titulo):
    """Gera gráficos individuais para Array e LinkedList"""
    os.makedirs("graficos/array", exist_ok=True)
    os.makedirs("graficos/linkedlist", exist_ok=True)
    
    df = pd.read_csv(os.path.join("resultados", nome_csv))
    
    # Separar dados por tipo
    dados_array = df[df["estrutura"].str.contains("Array")]
    dados_linked = df[df["estrutura"].str.contains("LinkedList")]
    
    # Gráficos para Array
    if not dados_array.empty:
        for operacao in ["adicionar", "remover", "aumentar", "diminuir"]:
            plt.figure(figsize=(8, 5))
            
            for estrutura in dados_array["estrutura"].unique():
                dados_estrutura = dados_array[dados_array["estrutura"] == estrutura]
                plt.plot(dados_estrutura["n"], dados_estrutura[operacao], 
                        label=estrutura, marker='o', markersize=3)
            
            plt.title(f"{titulo} - ARRAY ({operacao})")
            plt.xlabel("Tamanho de N")
            plt.ylabel("Tempo (segundos)")
            plt.legend()
            plt.grid(True)
            nome_img = f"array_{titulo.lower()}_{operacao}.png".replace(" ", "_")
            plt.savefig(os.path.join("graficos/array", nome_img))
            plt.close()
        
        print(f" Gráficos individuais de ARRAY para {titulo} gerados em /graficos/array")
    
    # Gráficos para LinkedList
    if not dados_linked.empty:
        for operacao in ["adicionar", "remover", "aumentar", "diminuir"]:
            plt.figure(figsize=(8, 5))
            
            for estrutura in dados_linked["estrutura"].unique():
                dados_estrutura = dados_linked[dados_linked["estrutura"] == estrutura]
                plt.plot(dados_estrutura["n"], dados_estrutura[operacao], 
                        label=estrutura, marker='o', markersize=3)
            
            plt.title(f"{titulo} - LINKEDLIST ({operacao})")
            plt.xlabel("Tamanho de N")
            plt.ylabel("Tempo (segundos)")
            plt.legend()
            plt.grid(True)
            nome_img = f"linkedlist_{titulo.lower()}_{operacao}.png".replace(" ", "_")
            plt.savefig(os.path.join("graficos/linkedlist", nome_img))
            plt.close()
        
        print(f" Gráficos individuais de LINKEDLIST para {titulo} gerados em /graficos/linkedlist")


def gerar_graficos_por_operacao():
    """Gera gráficos agrupando todas as estruturas por operação"""
    os.makedirs("graficos/por_operacao", exist_ok=True)
    
    # Ler todos os CSVs
    arquivos = ["pilha.csv", "fila.csv", "lista.csv"]
    dados_completos = []
    
    for arquivo in arquivos:
        caminho = os.path.join("resultados", arquivo)
        if os.path.exists(caminho):
            df = pd.read_csv(caminho)
            dados_completos.append(df)
    
    if not dados_completos:
        return
        
    df_completo = pd.concat(dados_completos, ignore_index=True)
    
    for operacao in ["adicionar", "remover", "aumentar", "diminuir"]:
        plt.figure(figsize=(10, 6))
        
        for estrutura in df_completo["estrutura"].unique():
            dados = df_completo[df_completo["estrutura"] == estrutura]
            plt.plot(dados["n"], dados[operacao], label=estrutura, marker='o', markersize=2)
        
        plt.title(f"Todas as Estruturas - Operação: {operacao}")
        plt.xlabel("Tamanho de N")
        plt.ylabel("Tempo (segundos)")
        plt.legend()
        plt.grid(True)
        nome_img = f"todas_estruturas_{operacao}.png"
        plt.savefig(os.path.join("graficos/por_operacao", nome_img))
        plt.close()
    
    print(" Gráficos por operação gerados em /graficos/por_operacao")


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
        
        # Gerar todos os tipos de gráficos
        titulo = nome_arquivo.replace(".csv", "").capitalize()
        gerar_graficos_comparacao(nome_arquivo, titulo)  # Gráficos comparativos
        gerar_graficos_individual(nome_arquivo, titulo)  # Gráficos individuais
    
    # Gerar gráficos agrupados por operação
    gerar_graficos_por_operacao()
    
    print("\n Testes concluídos com sucesso!")
    print(" Gráficos gerados:")
    print("   - /graficos/comparacao: Comparações Array vs LinkedList")
    print("   - /graficos/array: Gráficos individuais das estruturas Array")
    print("   - /graficos/linkedlist: Gráficos individuais das estruturas LinkedList")
    print("   - /graficos/por_operacao: Todas as estruturas agrupadas por operação")
