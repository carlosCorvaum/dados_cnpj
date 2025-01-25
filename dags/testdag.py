from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import os
import sys
import pandas as pd
from minio import Minio
from minio.error import S3Error
from io import BytesIO


def test():
    # Dados para o DataFrame
    dados = {
        "CNPJ": ["12345678000195", "98765432000100", "45678901000123"],
        "Razão Social": ["Empresa A", "Empresa B", "Empresa C"],
        "Atividade": ["Comércio", "Serviços", "Indústria"],
    }

    # Criar o DataFrame
    df = pd.DataFrame(dados)

    # Nome do bucket e destino do arquivo
    bucket_name = "coleta-dados-abertos-cnpj"
    destination_file = "aopa.csv"

    # Criar o cliente do MinIO
    client = Minio(
        "host.docker.internal:9000",  # Porta correta para a API do MinIO
        access_key="ZEZQi4iz62AvZ31OQhy5",
        secret_key="NfpavGez5hAi1dFEswYIr5blz6QcVD65P5IliVaR",
        secure=False,  # Use True se estiver usando HTTPS
    )

    # Verificar se o bucket existe e criá-lo se necessário
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' criado com sucesso.")
    else:
        print(f"Bucket '{bucket_name}' já existe.")

    # Criar um buffer de bytes em memória e salvar o CSV lá
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_buffer.seek(0)  # Retornar o cursor para o início do arquivo em memória

    # Realizar o upload diretamente do buffer para o MinIO
    client.put_object(
        bucket_name,  # Nome do bucket
        destination_file,  # Nome do arquivo no bucket
        csv_buffer,  # Objeto em memória
        length=csv_buffer.getbuffer().nbytes,  # Tamanho do arquivo
        content_type="text/csv",  # Tipo de conteúdo
    )

    print(
        f"Arquivo enviado com sucesso para o bucket '{bucket_name}' como '{destination_file}'."
    )


default_args = {
    "owner": "Corvaum",
    "start_date": datetime(2022, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(seconds=15),
}
# teste
with DAG(
    "TESTANDO",
    default_args=default_args,
    schedule_interval="0 0 10 * *",
    catchup=False,
) as dag:

    test_task = PythonOperator(
        task_id="test",
        python_callable=test,
        dag=dag,
    )

    test_task
