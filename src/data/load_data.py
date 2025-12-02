import pandas as pd
import os

def carregar_dados():
    """
    Lê o arquivo dados.csv que deve estar na pasta raiz do projeto.
    Retorna um DataFrame pandas.
    """
    caminho = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "dados.csv")

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo dados.csv não encontrado no caminho: {caminho}")

    return pd.read_csv(caminho)
