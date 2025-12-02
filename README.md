# Analise de Dados — Dashboard (Dash)

Este repositório foi preparado para transformar seus CSVs em um dashboard interativo no estilo Power BI usando Dash (Plotly + Dash).

## O que inclui
- Estrutura de projeto profissional
- Dash app em `src/dashboard/app.py`
- Scripts de carregamento e limpeza: `src/data/load_data.py`, `src/data/cleaning.py`
- Dados originais em `data/raw/`
- Dados processados em `data/processed/`
- Exemplos de gráficos em `reports/screenshots/`

## Como rodar localmente
1. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```
2. Instale dependências:
```bash
pip install -r requirements.txt
```
3. Rode o app:
```bash
python src/dashboard/app.py
```
4. Abra `http://localhost:8050`

## Observações
- O app carrega os arquivos de `data/processed/`. Caso tenha novas versões dos CSVs, coloque em `data/raw/` e reexecute o processo de limpeza (ainda básico).
- Os arquivos foram limpos de forma simples (padronização de nomes de colunas e tentativa de parse de datas). Ajustes específicos podem ser feitos em `src/data/cleaning.py`.

## Para a candidatura Gupy
Adicione prints do dashboard em `reports/screenshots` e atualize o README com um resumo do seu papel, tecnologias e insights principais. Posso ajudar a preparar esse texto com tom profissional.

