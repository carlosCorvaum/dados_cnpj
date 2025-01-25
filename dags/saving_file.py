from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os
from datetime import datetime


# Função para gerar e salvar o CSV
import traceback

def gerar_csv():
    print("testanaado")
    try:
        dados = {
            "CNPJ": ["12345678000195", "98765432000100", "45678901000123"],
            "Razão Social": ["Empresa A", "Empresa B", "Empresa C"],
            "Atividade": ["Comércio", "Serviços", "Indústria"],
        }

        df = pd.DataFrame(dados)

        caminho_arquivo = "G:/Airflow/logs/teste.csv"

        # Verificar e criar o diretório, se necessário
        dir_name = os.path.dirname(caminho_arquivo)
        os.makedirs(dir_name, exist_ok=True)

        # Verificando se o diretório foi criado corretamente
        if os.path.exists(dir_name):
            print(f"Diretório criado com sucesso: {dir_name}")
        else:
            print(f"Falha ao criar diretório: {dir_name}")

        # Salvar o arquivo CSV
        df.to_csv(caminho_arquivo, index=False)
        print(f"Arquivo salvo em {caminho_arquivo}")

    except Exception as e:
        print(f"Erro ao gerar CSV: {e}")
        traceback.print_exc()

# Definição do DAG
dag = DAG(
    "gerar_csv_dados_abertos_cnpj",
    description="DAG que gera um CSV com dados de empresas e salva em um diretório específico",
    schedule_interval="@daily",  # Executa diariamente
    start_date=datetime(2025, 1, 19),
    catchup=False,
)

# Definição do PythonOperator
gerar_csv_task = PythonOperator(task_id="gerar_csv", python_callable=gerar_csv, dag=dag)

# Definindo a sequência de execução
gerar_csv_task
