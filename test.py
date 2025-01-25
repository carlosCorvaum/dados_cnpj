import os
import pandas as pd


def gerar_csv():
    dir_name = "G:/Airlfow/volumes/dados_abertos_cnpj/empresa_dados"
    file_name = (
        "empresa_dados.csv"  # Certifique-se de que este é o nome correto do arquivo
    )
    file_path = os.path.join(dir_name, file_name)

    # Verificar se o diretório existe, caso contrário, criar
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
        print(f"Diretório criado com sucesso: {dir_name}")

    # Exemplo de dados fictícios a serem salvos no CSV
    data = {
        "CNPJ": ["12345678000123", "23456789000134"],
        "Nome Empresa": ["Empresa A", "Empresa B"],
    }
    df = pd.DataFrame(data)

    # Salvar o DataFrame como CSV
    try:
        df.to_csv(file_path, index=False)
        print(f"Arquivo salvo em {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")





def lerMinIo():


headers = {"User-Agent": "pandas"}
df = pd.read_csv(
    "https://download.bls.gov/pub/time.series/cu/cu.item",
    sep="\t",
    storage_options=headers
)




